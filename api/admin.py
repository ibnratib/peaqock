# IMPORTATIONS GENERAL

# IMPORTATION DJANGO
from django.contrib import admin

# IMPORTATION APPLICATION
import api.models as am

# importation django 
from import_export.admin import ImportExportModelAdmin


# definition des fonctions
def getFieldsModel(model):
    """
    cette fonction permet de retourner une liste
    de tous les champs d'une classe
    """
    return [field.name for field in model._meta.get_fields()] 


@admin.register(am.ComptesEspece)
class AdminCompte(ImportExportModelAdmin):
    list_display = (
        'client',
        'date_creation',
        'web',
        'etat') 
    list_filter = ("client",) # definir les champs de filtrage
    search_fields = ("client", ) # definir les champs de recherche

@admin.register(am.Client)
class AdminClient(ImportExportModelAdmin):
    list_display = (
        'user_id',
        'nature_client',
        'etat', 
        'raison_sociale',
        'matricule')
 # definire les chaps a afficher
    list_filter = ("user",) # definir les champs de filtrage


@admin.register(am.ImputationsEspeces)
class AdminClient(ImportExportModelAdmin):
    list_display = getFieldsModel(am.ImputationsEspeces) # definire les chaps a afficher
    list_filter = ("compte_espece",) # definir les champs de filtrage

@admin.register(am.User)
class AdminClient(ImportExportModelAdmin):
    list_display = ("id", "email", 'first_name', 'last_name') # definire les chaps a afficher



