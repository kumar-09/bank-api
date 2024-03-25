from django.urls import path
from accounts.views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



urlpatterns =[
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/',AccountCreateAPIView.as_view()),
    path('login/',MyLoginView.as_view()),
    path('transferFund/',TransferFundsView.as_view()),
    path('userdetail/<int:accountNo>/', UserDetailView.as_view()),
    path('transactions/', TransferFundsView.as_view()),
    path('applications/', ApplicationCreateAPIView.as_view(), name='application-create'),
    path('menu/', getmenu)
    
]

