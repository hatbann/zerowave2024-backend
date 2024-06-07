from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser
from django.db import models

class UserManager(BaseUserManager):
    use_in_migrations = True


    def create_user(self, nickname, email, password):
        user = self.model(
            nickname = nickname,
            email = email,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login_id=None, email=None, password=None, **extra_fields):
        superuser = self.create_user(
            login_id=login_id,
            email=email,
            password=password,
        )
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.is_active = True
        superuser.save(using=self._db)
        return superuser




# Create your models here.
class ZerowaveUser(AbstractBaseUser):
    nickname = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname', ]

    class Meta:
        db_table = 'zerowaveuser'

    def __str__(self): # 이 함수 추가
        return self.nickname  # Use