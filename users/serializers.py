from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, UserConfig

class UserConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserConfig
        fields = ['font_size', 'high_contrast', 'voice_guidance']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['phone', 'avatar_url']

class UserDetailSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(
        source='profile.phone', 
        read_only=True,
        help_text="Número telefónico del usuario (extraído de su perfil)."
    )
    avatar_url = serializers.CharField(
        source='profile.avatar_url', 
        read_only=True,
        help_text="URL de la imagen de avatar o foto del usuario (extraído de su perfil)."
    )
    config = UserConfigSerializer(
        read_only=True,
        help_text="Configuraciones de accesibilidad asociadas al usuario."
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'avatar_url', 'config']

class LoginRequestSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        help_text="Nombre de usuario de la cuenta."
    )
    password = serializers.CharField(
        required=True, 
        write_only=True,
        help_text="Contraseña correspondiente de la cuenta."
    )

class LoginResponseSerializer(serializers.Serializer):
    message = serializers.CharField(
        help_text="Mensaje descriptivo del resultado de la autenticación."
    )
    token = serializers.CharField(
        help_text="Token de autenticación de Django REST Framework (DRF) para llamadas seguras."
    )
    user = UserDetailSerializer(
        help_text="Información detallada del usuario logueado con su perfil y configuración."
    )

class RegisterRequestSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        help_text="Nombre de usuario único para la nueva cuenta."
    )
    password = serializers.CharField(
        required=True, 
        write_only=True,
        help_text="Contraseña para la nueva cuenta (se cifrará antes de almacenar)."
    )
    email = serializers.EmailField(
        required=True,
        help_text="Dirección de correo electrónico única."
    )
    phone = serializers.CharField(
        required=False, 
        allow_blank=True, 
        default='',
        help_text="Número de teléfono de contacto (opcional)."
    )
    avatar_url = serializers.CharField(
        required=False, 
        allow_blank=True, 
        default='',
        help_text="URL de la imagen de avatar del perfil (opcional)."
    )
    font_size = serializers.ChoiceField(
        choices=['SMALL', 'MEDIUM', 'LARGE'], 
        required=False, 
        default='MEDIUM',
        help_text="Tamaño de tipografía inicial de accesibilidad (opcional, default: 'MEDIUM')."
    )
    high_contrast = serializers.BooleanField(
        required=False, 
        default=False,
        help_text="Indica si activa el contraste de colores elevado de accesibilidad (opcional, default: false)."
    )
    voice_guidance = serializers.BooleanField(
        required=False, 
        default=False,
        help_text="Indica si activa la asistencia auditiva por voz (opcional, default: false)."
    )

class RegisterResponseSerializer(serializers.Serializer):
    message = serializers.CharField(
        help_text="Mensaje descriptivo del resultado del registro."
    )
    token = serializers.CharField(
        help_text="Token de autenticación DRF generado automáticamente para la nueva cuenta."
    )
    user = UserDetailSerializer(
        help_text="Detalle completo del usuario creado con su perfil y accesibilidad inicializada."
    )

class ProfileUpdateSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=False,
        help_text="Nuevo correo electrónico del usuario (debe ser único)."
    )
    phone = serializers.CharField(
        required=False, 
        allow_blank=True,
        help_text="Nuevo número telefónico de contacto del usuario."
    )
    avatar_url = serializers.CharField(
        required=False, 
        allow_blank=True,
        help_text="Nueva URL de imagen de avatar del usuario."
    )
    font_size = serializers.ChoiceField(
        choices=['SMALL', 'MEDIUM', 'LARGE'], 
        required=False,
        help_text="Nuevo tamaño de tipografía de accesibilidad."
    )
    high_contrast = serializers.BooleanField(
        required=False,
        help_text="Nueva preferencia de alto contraste de accesibilidad."
    )
    voice_guidance = serializers.BooleanField(
        required=False,
        help_text="Nueva preferencia de guía por voz de accesibilidad."
    )

class ProfileUpdateResponseSerializer(serializers.Serializer):
    message = serializers.CharField(
        help_text="Mensaje descriptivo del resultado de la actualización."
    )
    user = UserDetailSerializer(
        help_text="Detalle completo del usuario actualizado con sus nuevos valores."
    )

class LogoutResponseSerializer(serializers.Serializer):
    message = serializers.CharField(
        help_text="Mensaje de confirmación del cierre de sesión y eliminación del token."
    )
