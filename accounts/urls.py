from django.urls import path
from accounts.views import AccountListView

urlpatterns =[
    path('register/',AccountListView.as_view()),
    
]