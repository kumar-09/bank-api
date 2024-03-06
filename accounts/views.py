from django.shortcuts import render
from .models import Account
from rest_framework.generics import ListAPIView
from .serializers import AccountSerializer

# Create your views here.
class AccountListView(ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
