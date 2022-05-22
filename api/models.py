# IMPORTATIONS GENERAL

# IMPORTATION DJANGO
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from api.managers import UserManager

# IMPORTATION REST_FRAMEWORK
from django_rest_passwordreset.signals import reset_password_token_created

# IMPORTATIONS APPLICATION
import api.common as ac

class User(AbstractUser):
    first_name = models.CharField(max_length=255, blank=False, null=False)
    last_name = models.CharField(max_length=255, blank=False, null=False)
    email = models.CharField(max_length=255, unique=True, blank=False, null=False)
    password = models.CharField(max_length=255, blank=False, null=False)
    role = models.CharField(choices=ac.TYPE_UTILISATEUR, max_length=255, blank=False, null=False)
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'password', 'role']
    objects = UserManager()


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nature_client = models.CharField(max_length=100)
    etat = models.CharField(max_length=100)
    raison_sociale = models.TextField(max_length=100)
    matricule = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.user.email


class ComptesEspece(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)
    web = models.CharField(max_length=100)
    etat = models.CharField(max_length=100)


class ImputationsEspeces(models.Model):
    compte_espece = models.ForeignKey(ComptesEspece, on_delete=models.CASCADE)
    montant = models.FloatField()
    sens = models.IntegerField()
    nature = models.CharField(max_length=100)
    etat = models.IntegerField()
    date_etat = models.DateTimeField()
    date_imputation = models.DateField()
    



# reset password
@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    send_mail(
        # Objet :
        "Password Reset",
        # message:

        f"code de confirmation est : {reset_password_token.key}",
        # de :
        "ibnouratib.youssef@gmail.com",
        # à :
        [reset_password_token.user.email]
    )
