from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from django.contrib.auth import login, logout
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404
from .models import *
from .serializers import *

# Expected status codes:
# 200 request succeeded
# 201 request succeeded added a new resource
# 204 request succeeded no content being returned

# 400 client error
# 401 authentication error
# 403 server refused to authorize request

class HomeView(APIView): # Access / route | READ

    def get(self, request):
        try:
            return Response({"message: Success!"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        
        
class SignUpView(APIView): # Access /signup route, adds a new user instance to database | READ, CREATE
    def get(self, request):
        serializer = SignUpSerializer()
        return Response(serializer.data)

    def post(self, request):
        serializer = SignUpSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=request.data['username'])
            user.set_password(request.data['password'])
            user.save()
            token = Token.objects.create(user=user)
            return Response({'message': 'User sign up successful!', "token": token.key, "user": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'message': 'Sign up was unsuccessful', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
class CheckSessionView(APIView): # Checks if there is a user, Access signup route | READ
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
        
class LoginView(APIView): # Access /login route, logs in user | READ
    def post(self, request):
        user = get_object_or_404(User, username = request.data['username'])
        if not user.check_password(request.data['password']):
            return Response(status=status.HTTP_404_NOT_FOUND)
        token, created = Token.objects.get_or_create(user = user)
        login(request, user)
        return Response({'message': 'User sign up successful!', "token": token.key, 'user': {
                    'id': user.id,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                }}, status=status.HTTP_200_OK)
        
class LogoutView(APIView): # Access /logout route, logs out user | DELETE

    def post(self, request):
        if request.user.is_authenticated:
            logout(request)
            return Response({"message": 'Logout successful'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": 'Logout unsuccessful, no active session'}, status=status.HTTP_400_BAD_REQUEST)
        
class ClockInView(APIView): # Access /clockin route, adds a timeclock instance to database | CREATE

    def post(self, request):
        serializer = TimeClockSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": 'Clock in succesful!', "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Clock in unsuccessful', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
class ClockOutView(APIView): # Access /clockout route, updates timeclock instance with that has id with a new clock_out field | UPDATE

    def patch(self, request, id):
        time_clock = TimeClock.objects.get(id=id)
        serializer = TimeClockSerializer(time_clock, data = request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": 'Clock out successful!', "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Clock out unsuccessful', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
class TimeSheetView(ListAPIView): # Access /timesheet route, shows the user's timeclock instances | READ
    
    serializer_class = TimeClockSerializer

    def get_queryset(self):
        user = self.request.user
        return TimeClock.objects.filter(employee=user) 