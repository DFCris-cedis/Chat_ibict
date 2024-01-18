
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import Permission, Group
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)


    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.first_name

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


class Test(models.Model):
    testId = models.AutoField(primary_key=True)
    phraseTest = models.CharField()
    title = models.CharField(max_length=200, default="vazio")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, to_field='email')
    # user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.phraseTest


class Noun(models.Model):
    nounId = models.AutoField(primary_key=True)
    nounText = models.CharField(max_length=1500)
    idSignificado = models.CharField(max_length=1500)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)


class DicionarioManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().using('postgres')


class Dicionario(models.Model):
    IDunico = models.IntegerField(primary_key=True)
    IDSignificado = models.IntegerField()
    Palavra = models.CharField(max_length=1500)
    objects = DicionarioManager()


class ResultML(models.Model):
    idML = models.IntegerField(primary_key=True)
    noun = models.CharField(max_length=1500)
    prevRFrang = models.CharField(max_length=1500)
    prevC50 = models.CharField(max_length=1500)
    prevRpart = models.CharField(max_length=1500)

    # def __str__(self):
    #     return self.prevRFtrad
