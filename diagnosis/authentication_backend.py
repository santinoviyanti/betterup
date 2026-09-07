from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Mencari user berdasarkan email
            user = get_user_model().objects.get(email=username)
            if user.check_password(password):
                return user  # Mengembalikan user jika password cocok
        except get_user_model().DoesNotExist:
            return None  # Jika user tidak ditemukan
        return None
