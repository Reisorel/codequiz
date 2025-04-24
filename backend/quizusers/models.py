# Supprimer cette ligne
# from django.db import models

from mongoengine import Document, EmailField, StringField, DateTimeField, BooleanField
from datetime import datetime
from django.contrib.auth.hashers import make_password, check_password

class QuizUser(Document):
    email         = EmailField(required=True, unique=True)
    username      = StringField(required=True, unique=True)
    password_hash = StringField(required=True)
    is_active     = BooleanField(default=True)  # Utile pour désactiver des comptes
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
