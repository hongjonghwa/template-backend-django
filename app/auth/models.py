from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)


class UserManager(BaseUserManager):
    def create_user(self, username, name, password=None):
        if not username:
            raise ValueError('Username must not be empty')

        user = self.model(username=username, name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username, password)
        user.role = 'ADMIN'
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):

    username = models.CharField(max_length=255, unique=True)

    role = models.CharField(default="USER")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 부가 정보
    name = models.CharField()
    email = models.EmailField()
    photoUrl = models.URLField()

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.role == 'ADMIN'
