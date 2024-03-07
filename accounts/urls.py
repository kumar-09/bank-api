from django.urls import path
from accounts.views import *



urlpatterns =[
    path('register/',AccountListView.as_view()),
    path('userdetail/<int:accountNo>/', UserDetailView.as_view()),
    
]

