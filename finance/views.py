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
    
    