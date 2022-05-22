# IMPORTATIONS PYTHON

# IMPORTATIONS DJANGO
from django.shortcuts import render
from django.db.models import Count, F, Value

# IMPORTATION DJANGO REST FRAMEWORK
from rest_framework_simplejwt.views import TokenObtainPairView

# IMPORTATIONS APP
import api.models as am
import api.serializers as asr


from .serializers import UserSerializer, TokenGetPairSerializer



class TokenGetPairView(TokenObtainPairView):
    serializer_class = TokenGetPairSerializer


# #####################################################

# class StandardResultsSetPagination(PageNumberPagination):
#     page_size = 3
#     page_size_query_param = 'page_size'
#     max_page_size = 10
#     def get_paginated_response(self, data):
#         user = self.request.user
#         nbr_total = am.Voiture.objects.filter(client = user).count()
#         nbr = am.Voiture.objects.filter(client=user,
#             ).values('nom').annotate(nbr = Count('nom')).annotate(
#                 prc = ExpressionWrapper(F('nbr')*100 / nbr_total, output_field=FloatField()))

#         return Response({
#             'next': self.get_next_link(),
#             'previous': self.get_previous_link(),
#             'count': self.page.paginator.count,
#             'nbr_kia': nbr,
#             'nbr_total': nbr_total,
#             'liste_voiture': data,
#             'total_page': self.page.paginator.num_pages
#         })



# class ArticleViewSet(viewsets.ModelViewSet):
#     queryset = Article.objects.all()
#     serializer_class = ArticleSerializer
#     permission_classes = [IsAuthenticated,]
#     authentication_classes = [JWTAuthentication]
#     pagination_class = StandardResultsSetPagination


#     def retrieve(self, request, pk=None):
#         queryset = Article.objects.filter(title=pk)
#         serializer = ArticleSerializer(queryset, many=True)
#         return Response(serializer.data)

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def test_view(request):
#     serializer = TestSerialazer(data=request.data)
#     if serializer.is_valid():
#         data = serializer.data
#         try:
#             print(data.get('non',"not exist"))
#         except Exception as e:
#             print(e)
#         if data.get('nom') == "ayoube":
#             return Response("haad siyed 3ziiiiiz o ghali", status=status.HTTP_200_OK)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         # serializer.get('nom','none')


# class VoitureViewSet(viewsets.ModelViewSet):
#     queryset = am.Voiture.objects.get_queryset().defer('client')
#     serializer_class = ser.VoitureSerialiser
#     permission_classes = [IsAuthenticated ]
#     authentication_classes = [JWTAuthentication]
#     pagination_class = StandardResultsSetPagination
#     def get_queryset(self):
#         user = self.request.user
#         return am.Voiture.objects.filter(client=user)


def client_dashboard(request):
    template = "client/index.html"
    return render(request, template, {})



