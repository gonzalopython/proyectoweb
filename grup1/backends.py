from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Intenta encontrar al usuario utilizando su dirección de correo electrónico
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None

        # Verifica la contraseña
        if user.check_password(password):
            return user

    def get_user(self, user_id):
        try:
            # Recupera al usuario por su ID
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
