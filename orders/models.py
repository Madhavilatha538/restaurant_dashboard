from django.db import models
from django.utils import timezone
from restaurant.models import Table, MenuItem

class Order(models.Model):
    class Status(models.TextChoices):
        PLACED = "placed", "Placed"
        IN_KITCHEN = "in_kitchen", "In Kitchen"
        SERVED = "served", "Served"
        CLOSED = "closed", "Closed"

    table = models.ForeignKey(Table, on_delete=models.PROTECT, related_name="orders")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PLACED)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_open(self) -> bool:
        return self.status != self.Status.CLOSED

    def __str__(self):
        return f"Order #{self.id} - Table {self.table.number}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    menu_item = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("order","menu_item")

    def line_total(self):
        return self.menu_item.price * self.quantity
