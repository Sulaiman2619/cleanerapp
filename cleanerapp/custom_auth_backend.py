from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from .models import Cleaner, Staff

User = get_user_model()

class CustomModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)
            
            # Check if the user is a cleaner
            if Cleaner.objects.filter(cleaner_name=username).exists():
                if user.check_password(password):
                    return user
            
            # Check if the user is a staff member
            if Staff.objects.filter(staff_name=username).exists():
                if user.check_password(password):
                    return user

        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
