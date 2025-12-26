from django.db import models
from django.utils import timezone
from restaurant.models import Table
from orders.models import Order

class Bill(models.Model):
    class Status(models.TextChoices):
        NOT_GENERATED = "not_generated", "Not Generated"
        PENDING_PAYMENT = "pending_payment", "Pending Payment"
        PAID = "paid", "Paid"

    table = models.ForeignKey(Table, on_delete=models.PROTECT, related_name="bills")
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name="bills")
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.PENDING_PAYMENT)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(default=timezone.now)
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Bill #{self.id} - Table {self.table.number} - {self.status}"
