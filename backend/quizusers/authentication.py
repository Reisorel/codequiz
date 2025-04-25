from rest_framework_simplejwt.authentication import JWTAuthentication
from quizusers.models import QuizUser
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed

class MongoJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        """
        Tente de trouver et de retourner un utilisateur en utilisant le token JWT validé.
        """
        try:
            user_id = validated_token['user_id']

            # Utilise mongoengine pour récupérer l'utilisateur
            user = QuizUser.objects.get(id=user_id)

            # Vérifie si l'utilisateur est actif
            if not user.is_active:
                raise AuthenticationFailed('Utilisateur inactif ou supprimé')

            return user
        except KeyError:
            raise InvalidToken('Token invalide - aucun identifiant utilisateur')
        except QuizUser.DoesNotExist:
            raise AuthenticationFailed('Utilisateur non trouvé')
