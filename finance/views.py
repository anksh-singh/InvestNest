from django.shortcuts import render
from django.http import JsonResponse
from .models import Product, Client, User, Purchase
import json
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
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
        if mobile and otp and role:
            if role in ['User', 'Advisor']:
                return JsonResponse({'message': f'{role} account created successfully.'}, status=status.HTTP_201_CREATED)
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
    
    
    
    