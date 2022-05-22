from django.contrib.auth.base_user import BaseUserManager
from rest_framework.pagination import PageNumberPagination


class UserManager(BaseUserManager):
    def create_superuser(self, email, password, first_name, last_name, role):
        user = self.model(
            email=self.normalize_email(email),
            role=role,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.is_superuser = True
        user.is_active = True
        user.is_staff = True
        user.set_password(password)
        user.save()
        return user


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000