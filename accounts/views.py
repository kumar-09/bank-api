from django.shortcuts import render
from .models import Account
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from .serializers import AccountSerializer
from django.http import HttpResponse,JsonResponse

# Create your views here.
class AccountListView(APIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get(self, request): 
        queryset = Account.objects.all()
        data = list(queryset.values())
        serializer_class = AccountSerializer 
        return JsonResponse(data, safe=False) 
  
    def post(self, request): 
  
        serializer = AccountSerializer(data=request.data) 
        if serializer.is_valid(raise_exception=True): 
            serializer.save() 
            return  JsonResponse(serializer.data, safe=False)

class UserDetailView(RetrieveAPIView):
    serializer_class = AccountSerializer
    queryset = Account.objects.all()
    lookup_field = "accountNo"
