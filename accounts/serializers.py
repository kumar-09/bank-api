from rest_framework import serializers
from .models import Account, Transaction, Application
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [ 'accountNo', 'name', 'fathers_name', 'mobile_no', 'dob', 'email', 'gender', 'accountType', 'profile_image', 'is_admin', 'accountOpened']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'