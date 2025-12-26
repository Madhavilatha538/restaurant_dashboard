from rest_framework.permissions import BasePermission

class IsInGroup(BasePermission):
    group_name = None
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        if not self.group_name:
            return False
        return request.user.groups.filter(name=self.group_name).exists()

class IsWaiter(IsInGroup):
    group_name = "Waiter"

class IsCashier(IsInGroup):
    group_name = "Cashier"

class IsManager(IsInGroup):
    group_name = "Manager"
