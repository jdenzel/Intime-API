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
