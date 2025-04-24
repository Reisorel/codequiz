from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from quizusers.serializers import SignupSerializer, LoginSerializer
from rest_framework.views import APIView
from quizusers.models import QuizUser

class SignupView(generics.GenericAPIView):
    # Désactive l'authentification pour cette vue
    permission_classes = [AllowAny]
    serializer_class = SignupSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # Crée l'utilisateur
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class LoginView(generics.GenericAPIView):
    # Désactive l'authentification pour cette vue
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

class UserListView(APIView):
    """Vue pour lister tous les utilisateurs"""

    def get(self, request):
        """Récupère la liste de tous les utilisateurs"""
        users = QuizUser.objects.all()

        # Liste pour stocker les données formatées
        users_data = []

        # Extraire les informations nécessaires de chaque utilisateur
        for user in users:
            users_data.append({
                'id': str(user.id),  # Conversion explicite en string
                'email': user.email,
                'username': user.username,
                'created_at': user.created_at.isoformat() if user.created_at else None
            })

        return Response(users_data)
