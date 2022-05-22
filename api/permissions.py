# IMPORTATION GENERAL

# IMPORTATION DJANGO

# IMPORTATION DJANGO REST FRAMEWORK
from rest_framework.permissions import BasePermission

# IMPORTATION APPLICATION


class IsClient(BasePermission):
    message = "vous n'avez pas la permission client !"

    def has_permission(self, request, view):
        if request.user.role == 'client':
            return True
        else:
            return False


class IsAdmin(BasePermission):
    message = "vous n'avez pas la permission admin !" 

    def has_permission(self, request, view):
        if request.user.role == 'admin':
            return True
        else:
            return False


class Iscontroller(BasePermission):
    message = "vous n'avez pas la permission controleur !" 

    def has_permission(self, request, view):
        if request.user.role == 'controlleur':
            return True
        else:
            return False


class IsCreateurClient(BasePermission):
    message = "vous n'avez pas la permission createur client !" 

    def has_permission(self, request, view):
        if request.user.role == 'createur_client':
            return True
        else:
            return False
