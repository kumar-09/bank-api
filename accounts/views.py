from rest_framework.decorators import api_view
from rest_framework import status
from .models import Account, Transaction
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.views import APIView
from .serializers import *
from django.http import JsonResponse
from rest_framework.response import Response

# Create your views here.
class AccountCreateAPIView(CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        # Generate unique accountNo
        last_account = Account.objects.order_by('accountNo').last()
        if last_account:
            new_accountNo = last_account.accountNo + 1
        else:
            new_accountNo = 111111111111  # Start from this number or adjust as needed

        # Add accountNo to request data
        data['accountNo'] = new_accountNo

        # Check for duplication of mobile_no
        mobile_no = data.get('mobile_no')
        if mobile_no and Account.objects.filter(mobile_no=mobile_no).exists():
            return Response({'error': 'Mobile number already exists'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        accountNo = new_accountNo
        description = 'Account opening money'
        amount = 10000
        try:
            account = Account.objects.get(accountNo=accountNo)

            # Create initial transaction for account opening money
            Transaction.objects.create(
                accountNo=account,
                description=description,
                credit=amount,
                balance=amount
            )

        except Account.DoesNotExist:
            return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)
        user = Account.objects.get(accountNo=accountNo)
        serialized_user = LoginSerializer(user).data
        return Response(serialized_user, status=status.HTTP_201_CREATED)

class MyLoginView(APIView):

    def post(self, request):
        accountNo = request.data.get('accountNo')
        password = request.data.get('password')

        try:
            user = Account.objects.get(accountNo=accountNo)
            if user.password==password:
                serialized_user = LoginSerializer(user).data
                return Response(serialized_user,status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)
        except Account.DoesNotExist:
            return Response({'error': 'Account not exist'}, status=status.HTTP_404_NOT_FOUND)

class TransferFundsView(APIView):
    def post(self, request):
        from_accountNo = request.data.get('from_accountNo')
        to_accountNo = request.data.get('to_accountNo')
        amount = request.data.get('amount')
        password = request.data.get('password')

        try:
            _from_account = Transaction.objects.filter(accountNo=from_accountNo).first()
            from_account = Account.objects.get(accountNo=from_accountNo)
            to_account = Account.objects.get(accountNo=to_accountNo)
        except Account.DoesNotExist:
            return Response({"error": "One or both of the accounts do not exist"}, status=status.HTTP_404_NOT_FOUND)

        if not from_account.check_password(password):
            return Response({"error": "Incorrect password"}, status=status.HTTP_401_UNAUTHORIZED)
        
        if _from_account.balance < int(amount):
            return Response({"error": "Insufficient balance"}, status=status.HTTP_400_BAD_REQUEST)

        # Create transaction for sender (debit)
        from_transaction = Transaction(
            accountNo=from_account,
            description=f"Transferred {amount} to Account No. {to_accountNo}",
            debit=amount
        )
        from_transaction.save()

        # Create transaction for receiver (credit)
        to_transaction = Transaction(
            accountNo=to_account,
            description=f"Received {amount} from Account No. {from_accountNo}",
            credit=amount
        )
        to_transaction.save()

        return Response({"success": "Funds transferred successfully"}, status=status.HTTP_201_CREATED)
    def get(self, request):
        accountNo = request.query_params.get('accountNo')
        if not accountNo:
            return Response({"error": "Please provide an account number"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            account = Account.objects.get(accountNo=accountNo)
            transactions = Transaction.objects.filter(accountNo=account)
            serialized_transactions = TransactionSerializer(transactions, many=True).data
            return Response(serialized_transactions, status=status.HTTP_200_OK)
        except Account.DoesNotExist:
            return Response({"error": "Account does not exist"}, status=status.HTTP_404_NOT_FOUND)

class ApplicationCreateAPIView(APIView):
    def post(self, request):
        accountNo = request.data.get('accountNo')
        application_type = request.data.get('application_type')
        # Check if an entry exists for the given accountNo and application_type
        existing_application = Application.objects.filter(accountNo=accountNo, application_type=application_type).first()

        if existing_application:
            if existing_application.status != 'pending':
                serializer = ApplicationSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error":"Last Application is Peding"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Create a new application entry
            serializer = ApplicationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    # # If an entry already exists, update the status to approved or rejected
    # existing_application.status = 'approved'  # Or set to 'rejected' as needed
    # existing_application.save()
    # serializer = ApplicationSerializer(existing_application)
    # return Response(serializer.data, status=status.HTTP_200_OK)
                
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

    
@api_view(['GET'])
def getmenu(request):
    Menulist = Account.objects.all()
    serializer = AccountSerializer(Menulist , many=True)
    return Response(serializer.data)
