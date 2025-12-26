from django.urls import re_path
from .consumers import DashboardConsumer, KitchenConsumer

websocket_urlpatterns = [
    re_path(r"ws/dashboard/$", DashboardConsumer.as_asgi()),
    re_path(r"ws/kitchen/$", KitchenConsumer.as_asgi()),
]
