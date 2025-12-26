from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone

class Migration(migrations.Migration):
    initial = True
    dependencies = [("restaurant", "0001_initial")]
    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("status", models.CharField(choices=[("placed","Placed"),("in_kitchen","In Kitchen"),("served","Served"),("closed","Closed")], default="placed", max_length=20)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("table", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="orders", to="restaurant.table")),
            ],
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("quantity", models.PositiveIntegerField(default=1)),
                ("menu_item", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="restaurant.menuitem")),
                ("order", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="items", to="orders.order")),
            ],
            options={"unique_together": {("order","menu_item")}},
        ),
    ]
