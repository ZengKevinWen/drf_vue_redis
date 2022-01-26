
from rest_framework.permissions import BasePermission
class MyPerssions(BasePermission):
    def has_permission(self, request, view):
        is_pessions = request.user.choices_type
        print(is_pessions)
        if int(is_pessions) != 1:
            return True
        return False