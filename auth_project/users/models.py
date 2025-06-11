from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

class Profile (models.Model):
    """
        Define os perfis disponiveis no sistema    
    """
    PROFILE_CHOICES = [
        {'admin', 'Administrador'},
        {'anfitriao', 'Anfitrião'},
        {'guest', "Convidado"},
    ]
    
    name = models.CharField(max_length=50, choices=PROFILE_CHOICES, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.get_name_display()
class MenuItem (models.Model):
    """ 
    Itens de menu associados a perfis
    """
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    icon = models.CharField(max_length=50, blank=True)
    order = models.PositiveBigIntegerField(default=0)
    profiles = models.ManyToManyField(Profile, related_name='menu_items')
    
    class Meta:
        ordering = ['order']
        
    def __str__(self):
        return self.name

class CustomUserManager (BaseUserManager):
    def create_user(self, email, full_name, password=None, profile_name="guest", **extra_fields):
        if not email:
                raise ValueError('O email é obrigatório')
        
        profile, _ = Profile.objects.get_or_create(name=profile_name)
        
        
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name,profile=profile, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, full_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser deve ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser deve ter is_superuser=True.')

        # Obter o perfil de admin
        admin_profile = Profile.objects.get(name='admin')
        extra_fields['profile'] = admin_profile

        user = self.model(
            email=email,
            full_name=full_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
# Create your models here.

class CustomUser (AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email
    profile = models.ForeignKey(
        Profile,
        on_delete=models.PROTECT,
        related_name='users',
        null=True,
        blank=True
    )

    @property
    def is_admin (self):
        return self.profile.name == 'admin'
    @property
    def is_anfitriao(self):
        return self.profile.name == 'anfitriao'
    @property 
    def is_anfitriao(self):
        return self.profile.name == 'anfitriao'

    @property
    def is_guest(self):
        return self.profile.name == 'guest'
class UserPermission(models.Model):
    name = models.CharField(max_length=255, unique=True)
    codename = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    