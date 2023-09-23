from django.shortcuts import render
from django.http import JsonResponse
from .models import Product, Client, User, Purchase
import json
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import status
import random, string

# Create your views here.

characters = string.ascii_letters + string.digits  
otp = ''.join(random.choice(characters) for _ in range(6))


class SignUpView(APIView):
    def post(self, request):
        data = json.load(request.body)
        mobile = data.get('mobile', None)
        otp = data.get('otp', None)
        role = data.get('role', None)
        token, created = Token.objects.get_or_create(user=user)
        if mobile and otp and role:
            if role in ['User', 'Advisor']:
                user = User.objects.create(mobile=mobile, role=role)
                token, created = Token.objects.get_or_create(user=user)
                return JsonResponse({'message': f'{role} account created successfully.', 'token': token.key}, status=status.HTTP_201_CREATED)
            else:
                return JsonResponse({'error': 'Invalid role specified.'}, status=status.HTTP_400_BAD_REQUEST)

        return JsonResponse({'error': 'Mobile number, OTP, and role are required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    
    
class AddClient(APIView):
    def post(self, request):
        data = json.load(request.body)
        name = data.get('name')
        mobile = data.get('mobile')

        if name and mobile:
            advisor = request.user 
            client = Client.objects.create(name=name, mobile=mobile, advisor=advisor)

            return JsonResponse({'message': 'Client added successfully.', 'client_id': client.id}, status=status.HTTP_201_CREATED)

        return JsonResponse({'error': 'Name and mobile number are required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    

class AdvisorClientsList(APIView):
    
    def get(self, request):
        advisor_id = request.GET.get('advisor_id')
        clients = Client.objects.filter(advisor=advisor_id)
        client_list = [{'client_id': client.id, 'name': client.name, 'mobile': client.mobile} for client in clients]
        return JsonResponse({'clients': client_list}, status=status.HTTP_200_OK)
    
    
    
class AddProduct(APIView):
    
    def post(self, request):
        data = json.loads(request.body)
        name = data.get('name')
        description = data.get('description')
        category_name = data.get('category')
        admin_id = data.get('admin_id')
        
        if name and description and category_name and admin_id:
        
            try:
                admin = User.objects.filter(id=admin_id, role='Admin').first()
            except User.DoesNotExist:
                    return JsonResponse({'error': 'Admin not found.'}, status=status.HTTP_404_NOT_FOUND)
                
            product = Product.objects.create(name=name, description=description, category=category_name, admin=admin)
            
            return JsonResponse({"message" : "Product added successfully!"}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'error': 'Name, description, category, and admin_id all fields are required.'}, status=status.HTTP_400_BAD_REQUEST)
    



class AdvisorPurchaseProduct(APIView):
    def post(self, request):
        advisor_id = request.POST.get('advisor_id')
        client_id = request.POST.get('client_id')
        product_id = request.POST.get('product_id')

        if advisor_id and client_id and product_id:
            try:
                advisor = User.objects.get(id=advisor_id, role='Advisor')
                client = Client.objects.get(id=client_id, advisor=advisor)
                product = Product.objects.get(id=product_id)
            except Exception as e:
                return JsonResponse({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
            
            purchase = Purchase.objects.create(advisor=advisor, client=client, product=product)


            product_link = f'https://example.com/product/{purchase.id}/'  

            return JsonResponse({'message': 'Product purchased successfully.', 'product_link': product_link}, status=status.HTTP_201_CREATED)

        return JsonResponse({'error': 'advisor_id, client_id, and product_id are required.'}, status=status.HTTP_400_BAD_REQUEST)
