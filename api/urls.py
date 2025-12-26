from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import TableViewSet, MenuItemViewSet, OrderViewSet, BillViewSet

router = DefaultRouter()
router.register(r"tables", TableViewSet, basename="tables")
router.register(r"menu", MenuItemViewSet, basename="menu")
router.register(r"orders", OrderViewSet, basename="orders")
router.register(r"bills", BillViewSet, basename="bills")

urlpatterns = [path("", include(router.urls))]
