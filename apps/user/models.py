from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    """用户模型"""

    role = models.CharField(null=False, max_length=32)
    token = models.CharField(null=False, max_length=64)



