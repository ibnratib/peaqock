# IMPORTATIONS GENERAL

# IMPORTATION DJANGO
from django.contrib.auth.models import update_last_login

# IMPORTATION REST FRAMEWORK
from rest_framework import serializers
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenObtainSerializer


# IMPORTATION D'APPLICATION
import api.models as am
import api.common as ac
import api.functions as afct


class TokenGetPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        """
        permet de valider les information recuperes
        """
        # verifier si l'utilisateur existe
        if not afct.user_existe(attrs['email']):
                self.error_messages['no_active_account']= "Email not exists !"
        else:
            self.error_messages['no_active_account'] = "Invalid password !"

        # generer les tokens (access and refresh)
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data["role"] = str(self.user.role)
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = am.User
        fields = ['password', 'email', 'first_name', 'last_name', "role"]
        extra_kwargs = {'password': {'write_only': True}, }

    def create(self, validated_data):
        """
        permet de creer un utilisateur
        """
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        instance.set_password(password)
        instance.save()
        return instance


class ClientSerializer(serializers.Serializer):
    # champs utilisateur
    nom = serializers.CharField(max_length=100)
    prenom = serializers.CharField(max_length=100)
    email = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)

    # champs client
    nature_client = serializers.CharField(max_length=100)
    etat = serializers.CharField(max_length=100)
    raison_sociale = serializers.CharField(max_length=100)
    matricule = serializers.CharField(max_length=100)

class CompteSerialiser(serializers.ModelSerializer):
    class Meta:
        model = am.ComptesEspece
        fields = ['id', 'client', 'etat', 'web']

class ImputationSerializer(serializers.ModelSerializer):
    class Meta:
        model = am.ImputationsEspeces
        fields = '__all__'
    
    def validate_montant(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "le montant doit etre strictement positif")
        return value

# class ComptesEspeceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = am.ComptesEspece
#         fields = '__all__'

# class ImputationsEspecesSerializer(serializers.ModelSerializer):




#########################################
# class ArticleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Article
#         fields = '__all__'
    
#     def validate_title(self, value):
#         if 'voiture' in value.lower():
#             raise serializers.ValidationError("le titre ne doit pa etre une voiture")
#         return value

#     def validate_description(self, value):
#         if len(value) < 2:
#             raise serializers.ValidationError("la description est tres courte")
#         return value

# class VoitureSerialiser(serializers.ModelSerializer):
#     class Meta:
#         model = am.Voiture
#         fields = '__all__'


# class TestSerialazer(serializers.Serializer):
#     nom = serializers.CharField(max_length=100)
#     prenom = serializers.CharField(max_length=100)
#     salaire =  serializers.FloatField(default = 0)

#     def validate_nom(self, value):
#         if value == "ayoub":
#             print('dddddddddddddddddddddddd')
#             raise serializers.ValidationError("haad khona maydkhooolx 3andi")
#         return value
#     def validate_salaire(self, value):
#         if value < 20 :
#             raise serializers.ValidationError("ma salaire ma walo")
#         return value
    
