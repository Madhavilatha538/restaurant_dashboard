from django.contrib import admin
from django.urls import path, include
from accounts import views as account_views
from restaurant.views import dashboard

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", account_views.login_view, name="login"),
    path("logout/", account_views.logout_view, name="logout"),
    path("", dashboard, name="dashboard"),
    path("restaurant/", include("restaurant.urls")),
    path("orders/", include("orders.urls")),
    path("billing/", include("billing.urls")),
    path("api/", include("api.urls")),
]
