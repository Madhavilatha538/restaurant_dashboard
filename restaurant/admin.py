from django.contrib import admin
from .models import Table, MenuItem

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ("number","capacity","status")
    list_filter = ("status",)
    search_fields = ("number",)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("name","category","price","is_available")
    list_filter = ("category","is_available")
    search_fields = ("name",)
