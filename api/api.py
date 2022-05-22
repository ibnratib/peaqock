# IMPORTATIONS GENERAL

# IMPORTATION DJANGO

# IMPORTATION DJANGO REST FRAMEWORK
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status, viewsets, generics


# IMPORTATION APPLICATION
import api.common as ac
import api.models as am
import api.functions as afct
import api.serializers as asr
import api.permissions as ap
import api.managers as amn


######################################################################
# API CLIENT
######################################################################

class ApiCreateClient(generics.CreateAPIView):
    # definition des permission , type d'authentification et le serializer
    authentication_classes = [JWTAuthentication]  # type d'authentification
    permission_classes = [
        IsAuthenticated,
        ap.IsCreateurClient | ap.IsAdmin]  # permission
    serializer_class = asr.ClientSerializer

    @swagger_auto_schema(operation_id="Creer client")
    def post(self, request, *args, **kwargs):
        """
        permet a l'admin et le createur de client de creer un client
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            # verifier si le client exist
            if afct.user_existe(data['email']):
                reponse = {"detail": ac.USER_EXIST}
                return Response(
                    reponse, status=status.HTTP_400_BAD_REQUEST)

            else:
                # creer un nouveau utilisateur avec le role client
                new_user = am.User()
                new_user.first_name = data['nom']
                new_user.last_name = data['prenom']
                new_user.email = data['email']
                new_user.password = data['password']
                new_user.role = 'client'
                new_user.save()

                # creer un nouveau client et l'associer a l'utilisateur cree
                new_client = am.Client()
                new_client.user = new_user
                new_client.nature_client = data['nature_client']
                new_client.etat = data['etat']
                new_client.raison_sociale = data['raison_sociale']
                new_client.matricule = data['matricule']
                new_client.save()
                return Response(
                    {"detail": f"le client {data['prenom']} a été créé avec success"},
                    status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiModifierClient(generics.UpdateAPIView):
    # definition des permission , type d'authentification et le serializer
    authentication_classes = [JWTAuthentication]  # type d'authentification
    permission_classes = [
        IsAuthenticated,
        ap.IsCreateurClient | ap.IsAdmin]  # permission
    serializer_class = asr.ClientSerializer
    http_method_names = ['put']

    @swagger_auto_schema(operation_id="Modifier client")
    def put(self, request, client_id):

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            # verifier si le client exist
            if not am.Client.objects.filter(id=client_id).exists():
                reponse = {"detail": ac.USER_NOT_EXIST}
                return Response(
                    reponse, status=status.HTTP_404_NOT_FOUND)

            else:
                client = am.Client.objects.get(id=client_id)
                user = client.user
                # modifier les information client
                am.Client.objects.filter(id=client_id).update(
                    nature_client=data['nature_client'],
                    etat=data['etat'],
                    raison_sociale=data['raison_sociale'],
                    matricule=data['matricule']
                )

                # modifier l'infos user
                if data['nom']:
                    am.User.objects.filter(
                        id=user.id).update(
                            first_name=data['nom'])

                if data['prenom']:
                    am.User.objects.filter(
                        id=user.id).update(
                        last_name=data['prenom'])

                if data['email']:
                    if not am.User.objects.filter(
                        email=data['email']).exclude(
                            email=user.email).exists():
                        am.User.objects.filter(
                            id=user.id).update(
                            first_name=data['email'])
                    else:
                        reponse = {"detail": ac.USER_EXIST}
                        return Response(reponse,
                                        status=status.HTTP_400_BAD_REQUEST)

                if data['password']:
                    am.User.objects.filter(
                        id=user.id).update(
                        password=data['password'])

                return Response(
                    {"detail": f'client {user.first_name} est modifier avec success !'},
                    status=status.HTTP_200_OK)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiDeleteClient(generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication]  # type d'authentification
    permission_classes = [
        IsAuthenticated,
        ap.IsCreateurClient | ap.IsAdmin]

    @swagger_auto_schema(operation_id="Supprimer client")
    def destroy(self, request, client_id):
        """
        allows you to delete a customer
        """

        # verifier si le client exist
        if not am.Client.objects.filter(id=client_id).exists():
            reponse = {"detail": ac.USER_NOT_EXIST}
            return Response(
                reponse, status=status.HTTP_404_NOT_FOUND)
        else:
            client = am.Client.objects.get(id=client_id)
            user = client.user
            client.delete()
            am.User.objects.get(id=user.id).delete()
            return Response(
                'Client has been successfully deleted !',
                status=status.HTTP_200_OK)


class ApiListeClient(generics.ListAPIView):

    authentication_classes = [JWTAuthentication]  # type d'authentification
    permission_classes = [
        IsAuthenticated,
        ap.IsCreateurClient | ap.IsAdmin | ap.IsClient | ap.Iscontroller
    ]
    pagination_class = amn.StandardResultsSetPagination

    def get(self, request):
        list_user = afct.user_client_list()
        if self.request.user.role == 'client':
            user = list_user.filter(
                client_id=am.Client.objects.get(user=self.request.user).id)
            return Response(user, status=status.HTTP_200_OK)
        page = self.paginate_queryset(list_user)
        return self.get_paginated_response(page)


class ApiDetailClient(generics.RetrieveAPIView):

    authentication_classes = [JWTAuthentication]  # type d'authentification
    permission_classes = [
        IsAuthenticated,
        ap.IsCreateurClient | ap.IsAdmin | ap.IsClient | ap.Iscontroller
    ]
    pagination_class = amn.StandardResultsSetPagination

    @swagger_auto_schema(operation_id="Get details client")
    def get(self, request, client_id):
        """
        returns customer information
        """
        list_user = afct.user_client_list()
        if self.request.user.role == 'client':
            user = list_user.filter(
                client_id=am.Client.objects.get(user=self.request.user).id)
            return Response(user, status=status.HTTP_200_OK)
        else:
            list_user = list_user.filter(client_id=client_id)
            print(list_user)
        return Response(list_user, status=status.HTTP_200_OK)


######################################################################
######################################################################
# API COMPTE
######################################################################
######################################################################


class ApiCreateCompte(generics.CreateAPIView):
    # definition des permission , type d'authentification et le serializer
    authentication_classes = [JWTAuthentication]  # type d'authentification
    permission_classes = [
        IsAuthenticated,
        ap.IsCreateurClient | ap.IsAdmin]  # permission
    serializer_class = asr.CompteSerialiser

    @swagger_auto_schema(operation_id="Creer Compte")
    def post(self, request, *args, **kwargs):
        """
        permet a l'admin et le createur de client de creer un Compte
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            # verifier si le client exist
            if not am.Client.objects.filter(id=data['client'].id).exists():
                reponse = {"detail": ac.USER_NOT_EXIST}
                return Response(
                    reponse, status=status.HTTP_404_NOT_FOUND)

            else:
                # creer un nouveau compte
                client = am.Client.objects.get(id=data['client'].id)
                compte_espece = am.ComptesEspece()
                compte_espece.client = client
                compte_espece.web = data['web']
                compte_espece.etat = data['etat']
                compte_espece.save()
                return Response({'detail': ac.COMPTE_CREE}, status=status.HTTP_200_OK)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiModifierCompte(generics.UpdateAPIView):
    # definition des permission , type d'authentification et le serializer
    authentication_classes = [JWTAuthentication]  # type d'authentification
    permission_classes = [
        IsAuthenticated,
        ap.IsCreateurClient | ap.IsAdmin]  # permission
    serializer_class = asr.CompteSerialiser
    http_method_names = ['put']

    @swagger_auto_schema(operation_id="Modifier compte")
    def put(self, request, compte_id):

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data

            # verifier si le compte existe
            if am.ComptesEspece.objects.filter(id=compte_id).exists():

                # verifier si le client exist
                if not am.Client.objects.filter(id=data['client'].id).exists():
                    reponse = {"detail": ac.USER_NOT_EXIST}
                    return Response(
                        reponse, status=status.HTTP_404_NOT_FOUND)

                else:
                    # modifier le compte
                    am.ComptesEspece.objects.filter(
                        id=compte_id).update(
                            client=data['client'],
                            web=data['web'],
                            etat=data['etat']
                    )
                    return Response(
                        {'detail': ac.COMPTE_MODIFE}, status=status.HTTP_200_OK)
            else:
                reponse = {'detail': ac.COMPTE_NOT_EXIST}
                return Response(
                    reponse, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiDeleteCompte(generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication]  # type d'authentification
    permission_classes = [
        IsAuthenticated,
        ap.IsCreateurClient | ap.IsAdmin]

    @swagger_auto_schema(operation_id="Supprimer compte")
    def destroy(self, request, compte_id):
        """
        permet de supprimer un compte
        """
        # verifier si le compte exist
        if am.ComptesEspece.objects.filter(id=compte_id).exists():
            am.ComptesEspece.objects.filter(id=compte_id).delete()
            reponse = {"detail": ac.SUPPRIMER_COMPTE}
            return Response(reponse, status=status.HTTP_200_OK)
        else:
            reponse = {'detail': ac.COMPTE_NOT_EXIST}
            return Response(
                reponse, status=status.HTTP_404_NOT_FOUND)


class ApiListeCompte(generics.ListAPIView):

    authentication_classes = [JWTAuthentication]  # type d'authentification
    permission_classes = [
        IsAuthenticated,
        ap.IsCreateurClient | ap.IsAdmin | ap.IsClient | ap.Iscontroller
    ]
    pagination_class = amn.StandardResultsSetPagination
    serializer_class = asr.CompteSerialiser

    @swagger_auto_schema(operation_id="list comptes")
    def get(self, request):
        """
        permet de lister tout le comptes
        """
        list_compte = am.ComptesEspece.objects.all()
        if self.request.user.role == 'client':
            list_compte = list_compte.filter(
                client=am.Client.objects.get(user=self.request.user).id)
            serializer = self.get_serializer(list_compte, many=True)
            page = self.paginate_queryset(serializer.data)
            return self.get_paginated_response(page)
        serializer = self.get_serializer(list_compte, many=True)
        page = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(page)


class ApiDetailCompte(generics.RetrieveAPIView):

    authentication_classes = [JWTAuthentication]  # type d'authentification
    permission_classes = [
        IsAuthenticated,
        ap.IsCreateurClient | ap.IsAdmin | ap.IsClient | ap.Iscontroller
    ]
    pagination_class = amn.StandardResultsSetPagination
    serializer_class = asr.CompteSerialiser

    @swagger_auto_schema(operation_id="Detail compte")
    def get(self, request, compte_id):
        """
        returner le detail de compte
        """
        if am.ComptesEspece.objects.filter(id=compte_id).exists():
            compte = am.ComptesEspece.objects.get(id=compte_id)
            serializer = self.get_serializer(compte)

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            reponse = {'detail': ac.COMPTE_NOT_EXIST}
            return Response(
                reponse, status=status.HTTP_404_NOT_FOUND)

######################################################################
######################################################################
# API TRANSACTION
######################################################################
######################################################################


class ApiCreateTransaction(generics.CreateAPIView):
    # definition des permission , type d'authentification et le serializer
    authentication_classes = [JWTAuthentication]  # type d'authentification
    permission_classes = [
        IsAuthenticated,
        ap.IsClient | ap.IsAdmin]  # permission
    serializer_class = asr.ImputationSerializer

    @swagger_auto_schema(operation_id="Creer transaction")
    def post(self, request, *args, **kwargs):
        """
        permet a l'admin et les client de creer une transaction
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            # verifier si le client exist
            if not am.ComptesEspece.objects.filter(id=data['compte_espece'].id).exists():
                reponse = {"detail": ac.COMPTE_NOT_EXIST}
                return Response(
                    reponse, status=status.HTTP_404_NOT_FOUND)
            else:
                serializer.save()
                reponse = {"detail": ac.TRANSACTION_CREE}
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiDeleteTransaction(generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication]  # type d'authentification
    permission_classes = [
        IsAuthenticated,
        ap.IsCreateurClient | ap.IsAdmin]

    @swagger_auto_schema(operation_id="Supprimer Transaction")
    def destroy(self, request, transaction_id):
        """
        permet de supprimer une transaction .....
        """
        # verifier si le compte exist
        if am.ImputationsEspeces.objects.filter(id=transaction_id).exists():
            am.ImputationsEspeces.objects.filter(id=transaction_id).delete()
            reponse = {"detail": ac.TRANSACTION_SUPPRIME}
            return Response(reponse, status=status.HTTP_200_OK)
        else:
            reponse = {'detail': ac.TRANSACTION_NOT_EXIST}
            return Response(
                reponse, status=status.HTTP_404_NOT_FOUND)


class ApiListeTransaction(generics.ListAPIView):

    authentication_classes = [JWTAuthentication]  # type d'authentification
    permission_classes = [
        IsAuthenticated,
        ap.IsAdmin | ap.IsClient | ap.Iscontroller
    ]
    pagination_class = amn.StandardResultsSetPagination
    serializer_class = asr.ImputationSerializer

    @swagger_auto_schema(operation_id="list Transaction")
    def get(self, request):
        """
        permet de lister tout le comptes
        """
        transactions = am.ImputationsEspeces.objects.all()
        if self.request.user.role == 'client':
            transactions = afct.list_transaction_client(request.user)
            serializer = self.get_serializer(transactions, many=True)
            page = self.paginate_queryset(serializer.data)
            return self.get_paginated_response(page)
        serializer = self.get_serializer(transactions, many=True)
        page = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(page)


class ApiDetailTransaction(generics.RetrieveAPIView):

    authentication_classes = [JWTAuthentication]  # type d'authentification
    permission_classes = [
        IsAuthenticated,
        ap.IsAdmin | ap.IsClient | ap.Iscontroller
    ]
    serializer_class = asr.ImputationSerializer

    @swagger_auto_schema(operation_id="Detail transaction")
    def get(self, request, transaction_id):
        """
        returner le detail de transaction
        """
        if am.ImputationsEspeces.objects.filter(id=transaction_id).exists():
            compte = am.ImputationsEspeces.objects.get(id=transaction_id)
            serializer = self.get_serializer(compte)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            reponse = {'detail': ac.TRANSACTION_NOT_EXIST}
            return Response(
                reponse, status=status.HTTP_404_NOT_FOUND)
