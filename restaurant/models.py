from django.db import models

class Table(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = "available", "Available"
        OCCUPIED = "occupied", "Occupied"
        BILL_REQUESTED = "bill_requested", "Bill Requested"
        CLOSED = "closed", "Closed"

    number = models.PositiveIntegerField(unique=True)
    capacity = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE)

    def __str__(self):
        return f"Table {self.number} ({self.capacity})"

class MenuItem(models.Model):
    class Category(models.TextChoices):
        STARTER = "Starter", "Starter"
        MAIN = "Main", "Main"
        DRINKS = "Drinks", "Drinks"
        DESSERT = "Dessert", "Dessert"

    name = models.CharField(max_length=150, unique=True)
    category = models.CharField(max_length=20, choices=Category.choices)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
