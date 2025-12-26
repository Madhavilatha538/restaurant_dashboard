from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Table, MenuItem
from .permissions import in_group
from django.contrib import messages

@login_required
def dashboard(request):
    tables = Table.objects.all().order_by("number")
    return render(request, "restaurant/dashboard.html", {"tables": tables})

@in_group("Manager")
def table_list(request):
    tables = Table.objects.all().order_by("number")
    return render(request, "restaurant/table_list.html", {"tables": tables})

@in_group("Manager")
def table_create(request):
    if request.method == "POST":
        number = int(request.POST["number"])
        capacity = int(request.POST["capacity"])
        Table.objects.create(number=number, capacity=capacity)
        messages.success(request, "Table created.")
        return redirect("table_list")
    return render(request, "restaurant/table_form.html")

@in_group("Manager")
def table_edit(request, table_id):
    table = get_object_or_404(Table, id=table_id)
    if request.method == "POST":
        table.number = int(request.POST["number"])
        table.capacity = int(request.POST["capacity"])
        table.status = request.POST.get("status", table.status)
        table.save()
        messages.success(request, "Table updated.")
        return redirect("table_list")
    return render(request, "restaurant/table_form.html", {"table": table})

@in_group("Manager")
def menu_list(request):
    items = MenuItem.objects.all().order_by("category","name")
    return render(request, "restaurant/menu_list.html", {"items": items})

@in_group("Manager")
def menu_create(request):
    categories = [c[0] for c in MenuItem.Category.choices]
    if request.method == "POST":
        MenuItem.objects.create(
            name=request.POST["name"].strip(),
            category=request.POST["category"],
            price=request.POST["price"],
            is_available=("is_available" in request.POST),
        )
        messages.success(request, "Menu item created.")
        return redirect("menu_list")
    return render(request, "restaurant/menu_form.html", {"categories": categories})

@in_group("Manager")
def menu_edit(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    categories = [c[0] for c in MenuItem.Category.choices]
    if request.method == "POST":
        item.name = request.POST["name"].strip()
        item.category = request.POST["category"]
        item.price = request.POST["price"]
        item.is_available = ("is_available" in request.POST)
        item.save()
        messages.success(request, "Menu item updated.")
        return redirect("menu_list")
    return render(request, "restaurant/menu_form.html", {"item": item, "categories": categories})
