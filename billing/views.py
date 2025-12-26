from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from django.conf import settings
from django.http import FileResponse

from restaurant.models import Table
from restaurant.permissions import in_group
from orders.models import Order
from .models import Bill
from .pdf import render_bill_pdf
from realtime.utils import broadcast_table_update
from decimal import Decimal

def _compute_bill(order: Order):
    subtotal = sum((oi.line_total() for oi in order.items.select_related("menu_item").all()), start=Decimal("0.00"))

    tax_rate = (Decimal(str(settings.BILL_TAX_PERCENT)) / Decimal("100"))
    tax = (subtotal * tax_rate).quantize(Decimal("0.01"))

    total = (subtotal + tax).quantize(Decimal("0.01"))
    return subtotal, tax, total

@in_group("Cashier")
@transaction.atomic
def generate_bill(request, table_id):
    table = get_object_or_404(Table, id=table_id)
    order = (Order.objects.filter(table=table).exclude(status=Order.Status.CLOSED).order_by("-created_at").first())
    if not order:
        messages.error(request, "No open order found for this table.")
        return redirect("dashboard")

    subtotal, tax, total = _compute_bill(order)
    bill, created = Bill.objects.get_or_create(
        table=table, order=order,
        defaults={"status": Bill.Status.PENDING_PAYMENT, "subtotal": subtotal, "tax_amount": tax, "total": total},
    )
    if not created:
        bill.subtotal, bill.tax_amount, bill.total = subtotal, tax, total
        bill.status = Bill.Status.PENDING_PAYMENT
        bill.save()

    messages.success(request, f"Bill #{bill.id} generated.")
    return redirect("bill_detail", bill_id=bill.id)

@in_group("Cashier")
def bill_detail(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    return render(request, "billing/bill_detail.html", {"bill": bill, "tax_percent": settings.BILL_TAX_PERCENT})

@in_group("Cashier")
@transaction.atomic
def mark_paid(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    bill.status = Bill.Status.PAID
    bill.paid_at = timezone.now()
    bill.save(update_fields=["status","paid_at"])

    # close order and free table
    bill.order.status = Order.Status.CLOSED
    bill.order.save(update_fields=["status"])

    bill.table.status = Table.Status.AVAILABLE
    bill.table.save(update_fields=["status"])
    broadcast_table_update(bill.table)

    messages.success(request, f"Bill #{bill.id} marked as PAID. Table now Available.")
    return redirect("dashboard")

@in_group("Cashier")
def bill_pdf(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id)
    buf = render_bill_pdf(bill)
    return FileResponse(buf, as_attachment=True, filename=f"bill_{bill.id}.pdf")
