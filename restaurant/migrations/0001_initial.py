from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Table",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("number", models.PositiveIntegerField(unique=True)),
                ("capacity", models.PositiveIntegerField()),
                ("status", models.CharField(choices=[("available", "Available"), ("occupied", "Occupied"), ("bill_requested", "Bill Requested"), ("closed", "Closed")], default="available", max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name="MenuItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=150, unique=True)),
                ("category", models.CharField(choices=[("Starter", "Starter"), ("Main", "Main"), ("Drinks", "Drinks"), ("Dessert", "Dessert")], max_length=20)),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("is_available", models.BooleanField(default=True)),
            ],
        ),
    ]
