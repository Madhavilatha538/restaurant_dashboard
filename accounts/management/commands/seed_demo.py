from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, User
from restaurant.models import Table, MenuItem
from decimal import Decimal

GROUPS = ["Waiter", "Cashier", "Manager"]

class Command(BaseCommand):
    help = "Seed demo users, groups, tables, and menu items."

    def handle(self, *args, **options):
        for g in GROUPS:
            Group.objects.get_or_create(name=g)

        def get_or_create_user(username, password, group):
            user, created = User.objects.get_or_create(username=username, defaults={"is_staff": True})
            if created:
                user.set_password(password)
                user.save()
            user.groups.add(Group.objects.get(name=group))
            return user

        get_or_create_user("waiter1", "waiter123", "Waiter")
        get_or_create_user("cashier1", "cashier123", "Cashier")
        mgr = get_or_create_user("manager1", "manager123", "Manager")
        mgr.is_superuser = True
        mgr.is_staff = True
        mgr.save()

        for i, cap in [(1,2),(2,4),(3,4),(4,6),(5,8)]:
            Table.objects.get_or_create(number=i, defaults={"capacity": cap})

        items = [
            ("Spring Rolls", "Starter", "120.00", True),
            ("Paneer Butter Masala", "Main", "260.00", True),
            ("Veg Biryani", "Main", "220.00", True),
            ("Lime Soda", "Drinks", "80.00", True),
            ("Gulab Jamun", "Dessert", "90.00", True),
        ]
        for name, cat, price, avail in items:
            MenuItem.objects.get_or_create(name=name, defaults={"category": cat, "price": Decimal(price), "is_available": avail})

        self.stdout.write(self.style.SUCCESS("Seeded demo data. Users: waiter1/cashier1/manager1"))
