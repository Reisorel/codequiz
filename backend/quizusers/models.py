from mongoengine import Document, EmailField, StringField, DateTimeField, BooleanField
from datetime import datetime
from django.contrib.auth.hashers import make_password, check_password

class QuizUser(Document):
    email         = EmailField(required=True, unique=True)
    username      = StringField(required=True, unique=True)
    password_hash = StringField(required=True)
    is_active     = BooleanField(default=True)  # CHAMP réel, pas une propriété
    created_at    = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'quizusers',
        'indexes': ['email', 'username']  # Pour optimiser les recherches
    }

    # Méthodes pour gérer les mots de passe de façon sécurisée
    def set_password(self, raw_password):
        self.password_hash = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password_hash)

    # Propriétés requises par DRF pour l'authentification
    @property
    def is_authenticated(self):
        return True  # L'utilisateur est toujours authentifié une fois récupéré

    # D'autres propriétés utiles pour la compatibilité avec Django
    def get_username(self):
        return self.username

    @property
    def is_anonymous(self):
        return False
