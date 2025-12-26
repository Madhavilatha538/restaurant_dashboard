from django.urls import path
from . import views

urlpatterns = [
    path("new/", views.order_create, name="order_create"),
    path("<int:order_id>/", views.order_detail, name="order_detail"),
    path("<int:order_id>/status/", views.order_update_status, name="order_update_status"),
    path("table/<int:table_id>/request-bill/", views.request_bill, name="request_bill"),
]
