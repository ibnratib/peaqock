# IMPORTATION PYTHON

# IMPORTATIONS DJANGO 
from django.urls import path, include, re_path

# IMPORTATIONS DJANGO REST FRAMEWORQUE
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from rest_framework.authentication import TokenAuthentication
from rest_framework.documentation import include_docs_urls

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


# IMPORTATIONS APP
import api.views as views
import api.api as api


urlpatterns = [
   # ENDPOINTS CLIENT
   path('client/create', api.ApiCreateClient.as_view(), name='create_client'),
   path('client/update/<int:client_id>', api.ApiModifierClient.as_view(),
         name='modifier_client'),
   path('client/delete/<int:client_id>', api.ApiDeleteClient.as_view(),
         name='supprimer_client'),
   path('client/list/', api.ApiListeClient.as_view(),
         name='list_client'),
   path('client/detail/<int:client_id>', api.ApiDetailClient.as_view(),
         name='detail_client'), 

   # ENDPOINTS COMPTE  
   path('compte/create', api.ApiCreateCompte.as_view(),
         name='create_compte'),   
   path('compte/update/<int:compte_id>', api.ApiModifierCompte.as_view(),
         name='update_compte'), 
   path('compte/delete/<int:compte_id>', api.ApiDeleteCompte.as_view(),
         name='delete_compte'), 
   path('compte/list', api.ApiListeCompte.as_view(),
         name='list_compte'),
   path('compte/detail/<int:compte_id>', api.ApiDetailCompte.as_view(),
         name='detail_compte'), 
   
   # ENDPOINTS TRANSACTIONS
   path('transaction/create', api.ApiCreateTransaction.as_view(),
      name='create_transaction'), 
   path('transaction/delete/<int:transaction_id>', api.ApiDeleteTransaction.as_view(),
      name='delete_transaction'), 
   path('transaction/list', api.ApiListeTransaction.as_view(),
      name='list_transaction'), 
   path('transaction/detail/<int:transaction_id>', api.ApiDetailTransaction.as_view(),
      name='detail_transaction'),      
]

schema_view = get_schema_view(
   openapi.Info(
      title="Documentation Debat",
      default_version='v1.0',
      description="Test description",
    #   contact=openapi.Contact(email="https://"),
     #  license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
   authentication_classes=[TokenAuthentication]
)

urlpatterns += [
   re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   re_path(r'^documentation_api/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]