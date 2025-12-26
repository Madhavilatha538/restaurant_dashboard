from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django.conf import settings
from django.utils import timezone

from restaurant.models import Table, MenuItem
from orders.models import Order, OrderItem
from billing.models import Bill
from .serializers import TableSerializer, MenuItemSerializer, OrderSerializer, BillSerializer
from .permissions import IsManager, IsWaiter, IsCashier
from realtime.utils import broadcast_table_update, broadcast_kitchen_new_order

class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all().order_by("number")
    serializer_class = TableSerializer
    permission_classes = [IsManager]

class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all().order_by("category","name")
    serializer_class = MenuItemSerializer
    permission_classes = [IsManager]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by("-created_at")
    serializer_class = OrderSerializer
    permission_classes = [IsWaiter]

    @transaction.atomic
    def perform_create(self, serializer):
        order = serializer.save()
        table = order.table
        if table.status == Table.Status.AVAILABLE:
            table.status = Table.Status.OCCUPIED
            table.save(update_fields=["status"])
            broadcast_table_update(table)
        broadcast_kitchen_new_order(order)

    @action(detail=True, methods=["post"])
    def status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get("status")
        if new_status in dict(Order.Status.choices):
            order.status = new_status
            order.save(update_fields=["status"])
        return Response(OrderSerializer(order).data)

class BillViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Bill.objects.all().order_by("-created_at")
    serializer_class = BillSerializer
    permission_classes = [IsCashier]

    @action(detail=False, methods=["post"], url_path="generate/(?P<table_id>\d+)")
    @transaction.atomic
    def generate(self, request, table_id=None):
        table = Table.objects.get(id=table_id)
        order = Order.objects.filter(table=table).exclude(status=Order.Status.CLOSED).order_by("-created_at").first()
        if not order:
            return Response({"detail":"No open order"}, status=400)
        subtotal = sum((oi.line_total() for oi in order.items.select_related("menu_item").all()), start=0)
        tax = subtotal * (settings.BILL_TAX_PERCENT / 100.0)
        total = subtotal + tax
        bill, _ = Bill.objects.get_or_create(table=table, order=order, defaults={"subtotal":subtotal,"tax_amount":tax,"total":total})
        bill.status = Bill.Status.PENDING_PAYMENT
        bill.subtotal, bill.tax_amount, bill.total = subtotal, tax, total
        bill.save()
        return Response(BillSerializer(bill).data)

    @action(detail=True, methods=["post"])
    @transaction.atomic
    def paid(self, request, pk=None):
        bill = self.get_object()
        bill.status = Bill.Status.PAID
        bill.paid_at = timezone.now()
        bill.save(update_fields=["status","paid_at"])
        bill.order.status = Order.Status.CLOSED
        bill.order.save(update_fields=["status"])
        bill.table.status = Table.Status.AVAILABLE
        bill.table.save(update_fields=["status"])
        broadcast_table_update(bill.table)
        return Response(BillSerializer(bill).data)
