from django.contrib.auth.models import User
from django.db import models


class Classroom(models.Model):
    def get_users(self, t): return self.accounts.filter(is_staff=t)
    name = models.CharField(max_length=255)
    description = models.TextField()
    accounts = models.ManyToManyField(User)
    def students(self): return self.get_users(False).all()
    def teachers(self): return self.get_users(True).all()


class Avatar(models.Model):
    account = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='avatars/')
