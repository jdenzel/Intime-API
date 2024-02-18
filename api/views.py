from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from django.contrib.auth import login, logout
from .models import *
from .serializers import *

class HomeView(APIView):
    def get(self, request):
        try:
            return Response({"message: Success!"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        
        
class SignUpView(APIView):
    def get(self, request):
        serializer = SignUpSerializer()
        return Response(serializer.data)

    def post(self, request):
        serializer = SignUpSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User sign up successful'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Sign up was unsuccessful', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
class CheckSessionView(APIView):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            
            return Response({'user': {
                    'id': user.id,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name}}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "No active session"}, status=status.HTTP_401_UNAUTHORIZED)
        
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            return Response({"message": 'Login succesful', 'user': {
                    'id': user.id,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                }}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Login unsuccesful', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)