from django.urls import path
from . import views

urlpatterns = [
    path("tables/", views.table_list, name="table_list"),
    path("tables/new/", views.table_create, name="table_create"),
    path("tables/<int:table_id>/edit/", views.table_edit, name="table_edit"),
    path("menu/", views.menu_list, name="menu_list"),
    path("menu/new/", views.menu_create, name="menu_create"),
    path("menu/<int:item_id>/edit/", views.menu_edit, name="menu_edit"),
]
