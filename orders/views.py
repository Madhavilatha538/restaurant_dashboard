from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.db import transaction
from django.contrib import messages

from restaurant.models import Table, MenuItem
from restaurant.permissions import in_group
from .models import Order, OrderItem
from .forms import OrderCreateForm, OrderItemForm
from realtime.utils import broadcast_table_update, broadcast_kitchen_new_order

@in_group("Waiter")
@transaction.atomic
def order_create(request):
    ItemFormSet = formset_factory(OrderItemForm, extra=3, min_num=1, validate_min=True, can_delete=True)
    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        formset = ItemFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            table = form.cleaned_data["table"]
            if table.status == Table.Status.AVAILABLE:
                table.status = Table.Status.OCCUPIED
                table.save(update_fields=["status"])
                broadcast_table_update(table)

            order = Order.objects.create(table=table, status=Order.Status.PLACED)

            for f in formset:
                if f.cleaned_data and not f.cleaned_data.get("DELETE", False):
                    menu_item = f.cleaned_data["menu_item"]
                    qty = f.cleaned_data["quantity"]
                    OrderItem.objects.update_or_create(order=order, menu_item=menu_item, defaults={"quantity": qty})

            broadcast_kitchen_new_order(order)
            messages.success(request, f"Order #{order.id} placed.")
            return redirect("order_detail", order_id=order.id)
    else:
        form = OrderCreateForm()
        formset = ItemFormSet()
    return render(request, "orders/order_create.html", {"form": form, "formset": formset})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    is_waiter = request.user.is_superuser or request.user.groups.filter(name="Waiter").exists()

    return render(
        request,
        "orders/order_detail.html",
        {"order": order, "is_waiter": is_waiter},
    )

@in_group("Waiter")
@transaction.atomic
def order_update_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == "POST":
        new_status = request.POST.get("status")
        if new_status in dict(Order.Status.choices):
            order.status = new_status
            order.save(update_fields=["status"])
            messages.success(request, "Order status updated.")
    return redirect("order_detail", order_id=order.id)

@in_group("Waiter")
@transaction.atomic
def request_bill(request, table_id):
    table = get_object_or_404(Table, id=table_id)
    if table.status in [Table.Status.OCCUPIED]:
        table.status = Table.Status.BILL_REQUESTED
        table.save(update_fields=["status"])
        broadcast_table_update(table)
        messages.success(request, f"Bill requested for Table {table.number}.")
    return redirect("dashboard")
