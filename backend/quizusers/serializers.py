# backend/quizusers/serializers.py

# Import du module serializers de Django REST Framework pour convertir les objets Python en format JSON
from rest_framework import serializers
# Import de la classe RefreshToken pour gérer les tokens JWT d'authentification
from rest_framework_simplejwt.tokens import RefreshToken
# Import du modèle MongoEngine pour les utilisateurs
from quizusers.models import QuizUser

# Définition du serializer pour l'inscription des utilisateurs
class SignupSerializer(serializers.Serializer):
    # Champ pour l'email, validé automatiquement comme un email valide
    email    = serializers.EmailField()
    # Champ pour le nom d'utilisateur, avec une longueur minimale et maximale
    username = serializers.CharField(min_length=3, max_length=150)
    # Champ pour le mot de passe, marqué write_only pour ne pas être renvoyé dans les réponses
    password = serializers.CharField(write_only=True, min_length=8)

    # Méthode personnalisée pour valider l'unicité de l'email
    def validate_email(self, value):
        # Vérifie si un utilisateur avec cet email existe déjà dans la base de données
        if QuizUser.objects(email=value).first():
            # Lève une exception si l'email est déjà utilisé
            raise serializers.ValidationError("Email déjà utilisé")
        return value

    # Méthode personnalisée pour valider l'unicité du nom d'utilisateur
    def validate_username(self, value):
        # Vérifie si un utilisateur avec ce nom existe déjà dans la base de données
        if QuizUser.objects(username=value).first():
            # Lève une exception si le nom d'utilisateur est déjà utilisé
            raise serializers.ValidationError("Username déjà utilisé")
        return value

    # Méthode pour créer un nouvel utilisateur après validation des données
    def create(self, validated_data):
        # Création d'une nouvelle instance du modèle QuizUser
        user = QuizUser(
            email=validated_data['email'],
            username=validated_data['username']
        )
        # Hashage sécurisé du mot de passe avant enregistrement
        user.set_password(validated_data['password'])
        # Sauvegarde de l'utilisateur dans la base de données
        user.save()
        # Renvoie l'instance utilisateur créée
        return user

    # Contrôle le format JSON de sortie lors de la sérialisation
    def to_representation(self, instance):
        """Contrôle le format JSON de sortie lors de la sérialisation"""
        # Création manuelle du token
        refresh = RefreshToken()
        # Stocke l'ID utilisateur comme string dans le token
        refresh['user_id'] = str(instance.id)

        # Retourne un dictionnaire contenant les informations utilisateur et les tokens
        return {
            'user': {
                'id':         str(instance.id),  # Convertit l'ID MongoDB en string
                'email':      instance.email,    # Email de l'utilisateur
                'username':   instance.username, # Nom d'utilisateur
                'created_at': instance.created_at.isoformat() # Date de création formatée
            },
            'tokens': {
                'access':  str(refresh.access_token),  # Token d'accès pour l'API
                'refresh': str(refresh)                # Token de rafraîchissement
            }
        }

# Définition du serializer pour la connexion des utilisateurs existants
class LoginSerializer(serializers.Serializer):
    # Champ pour l'email de connexion
    email    = serializers.EmailField()
    # Champ pour le mot de passe, marqué write_only pour ne pas être renvoyé
    password = serializers.CharField(write_only=True)

    # Méthode de validation qui vérifie les identifiants de connexion
    def validate(self, data):
        # Recherche l'utilisateur par email
        user = QuizUser.objects(email=data['email']).first()
        # Vérifie si l'utilisateur existe et si le mot de passe correspond
        if not user or not user.check_password(data['password']):
            # Lève une exception si les identifiants sont invalides
            raise serializers.ValidationError("Identifiants invalides")
        # Ajoute l'utilisateur trouvé aux données validées
        data['user'] = user
        return data

    # Contrôle le format JSON de sortie pour la connexion
    def to_representation(self, instance):
        """Contrôle le format JSON de sortie pour la connexion"""
        # Récupère l'utilisateur des données validées
        user = instance['user']

        # Création manuelle du token au lieu d'utiliser for_user
        refresh = RefreshToken()
        # Stocke l'ID utilisateur comme string dans le token
        refresh['user_id'] = str(user.id)

        # Retourne uniquement les tokens d'authentification
        return {
            'tokens': {
                'access':  str(refresh.access_token),
                'refresh': str(refresh)
            }
        }
