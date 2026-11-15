from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# Esta clase, contienen métodos que los crea y archiva (a los usuarios)
class UsuarioManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('el email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user       

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('rol', self.model.Rol.ADMIN)
        return self.create_user(email, password, **extra_fields)

# Esta clase define la forma (el formulario de datos)
class Usuario(AbstractUser):

    class Rol(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrador'
        USUARIO = 'USUARIO', 'Usuario'
        
    username = None
    email = models.EmailField(unique=True)
    rol = models.CharField(max_length=10, choices=Rol.choices, default=Rol.USUARIO)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UsuarioManager()
    
    def __str__(self):
        return self.email
# Create your models here.
