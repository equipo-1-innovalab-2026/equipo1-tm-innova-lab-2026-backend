from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='profile',
        help_text="Usuario Django propietario de este perfil."
    )
    
    # El hash biométrico queda como opcional (null=True, blank=True) para más adelante
    # bio_face_hash = models.TextField(null=True, blank=True) 
    avatar_url = models.CharField(
        max_length=255, 
        blank=True,
        help_text="URL de la imagen de avatar o foto de perfil del usuario."
    )
    phone = models.CharField(
        max_length=50, 
        blank=True,
        help_text="Número telefónico de contacto del usuario."
    )       
    
    def __str__(self):
        return f"Perfil de {self.user.username}"
    
    
class UserConfig(models.Model):
    
    # Opciones para el ENUM de font_size
    FONT_SIZE_CHOICES = [
        ('SMALL', 'Small'),
        ('MEDIUM', 'Medium'),
        ('LARGE', 'Large'),
    ]

    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='config',
        help_text="Usuario Django propietario de esta configuración."
    )
    font_size = models.CharField(
        max_length=10, 
        choices=FONT_SIZE_CHOICES, 
        default='MEDIUM',
        help_text="Tamaño de la tipografía preferida por el usuario para accesibilidad ('SMALL', 'MEDIUM', 'LARGE')."
    )
    high_contrast = models.BooleanField(
        default=False,
        help_text="Preferencia de visualización de colores con contraste elevado para accesibilidad."
    )
    voice_guidance = models.BooleanField(
        default=False,
        help_text="Preferencia de navegación asistida por comandos y locución de voz."
    )

    def __str__(self):
        return f"Configuración de {self.user.username}"


@receiver(post_save, sender=User)
def create_user_profile_and_config(sender, instance, created, **kwargs):
    if created:  
        UserProfile.objects.create(user=instance)
        UserConfig.objects.create(user=instance)
        
@receiver(post_save, sender=User)
def save_user_profile_and_config(sender, instance, **kwargs):
    # Usamos getattr por seguridad en caso de que no exista el perfil
    if hasattr(instance, 'profile'):
        instance.profile.save()
    if hasattr(instance, 'config'):
        instance.config.save()