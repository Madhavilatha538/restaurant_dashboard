from django.urls import path
from . import views

urlpatterns = [
    path("table/<int:table_id>/generate/", views.generate_bill, name="generate_bill"),
    path("<int:bill_id>/", views.bill_detail, name="bill_detail"),
    path("<int:bill_id>/paid/", views.mark_paid, name="mark_paid"),
    path("<int:bill_id>/pdf/", views.bill_pdf, name="bill_pdf"),
]
