import api.models as am
from django.db.models import Count, F, Value


def user_existe(email: str) -> bool:
    """
    cette fonction permet de verifier si un utilisateur exist ou pas
    """
    if am.User.objects.filter(email = email).exists():
        return True
    else:
        return False

def user_client_list() ->list:
    """
    permet de lister tout les client
    """
    users = am.Client.objects.filter(user__role="client").values(
            'etat',
            "nature_client",
            "etat",
            "raison_sociale",
            "matricule",
            client_id = F('id'),
            nom = F('user__first_name'),
            prenom = F('user__last_name'),
            email = F('user__email'),
            password = F('user__password'),
            )
    return users

def list_transaction_client(user):
    """
    permet de returner la list des tronsaction d'un client
    """
    client = am.Client.objects.get(user=user)
    comptes = am.ComptesEspece.objects.filter(client=client)
    transactions = am.ImputationsEspeces.objects.filter(compte_espece__in=comptes)
    return transactions
