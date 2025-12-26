from django.contrib import admin
from .models import Bill

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ("id","table","order","status","total","created_at","paid_at")
    list_filter = ("status",)
    search_fields = ("id","table__number","order__id")
