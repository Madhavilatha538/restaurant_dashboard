from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone

class Migration(migrations.Migration):
    initial = True
    dependencies = [("restaurant","0001_initial"), ("orders","0001_initial")]
    operations = [
        migrations.CreateModel(
            name="Bill",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("status", models.CharField(choices=[("not_generated","Not Generated"),("pending_payment","Pending Payment"),("paid","Paid")], default="pending_payment", max_length=30)),
                ("subtotal", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("tax_amount", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("total", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("paid_at", models.DateTimeField(blank=True, null=True)),
                ("order", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="bills", to="orders.order")),
                ("table", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="bills", to="restaurant.table")),
            ],
        ),
    ]
