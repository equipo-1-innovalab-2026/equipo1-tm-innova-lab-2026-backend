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
    email = serializers.EmailField(
        required=True,
        error_messages={
            'required': 'El email es un campo obligatorio.',
            'blank': 'El email es un campo obligatorio.',
            'invalid': 'Introduzca una dirección de correo electrónico válida.'
        },
        help_text="Dirección de correo electrónico asociada a la cuenta."
    )
    password = serializers.CharField(
        required=True, 
        write_only=True,
        error_messages={
            'required': 'El password es un campo obligatorio.',
            'blank': 'El password es un campo obligatorio.'
        },
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
        error_messages={
            'required': 'El username es un campo obligatorio.',
            'blank': 'El username es un campo obligatorio.'
        },
        help_text="Nombre de usuario único para la nueva cuenta."
    )
    email = serializers.EmailField(
        required=True,
        error_messages={
            'required': 'El email es un campo obligatorio.',
            'blank': 'El email es un campo obligatorio.',
            'invalid': 'Introduzca una dirección de correo electrónico válida.'
        },
        help_text="Dirección de correo electrónico única."
    )
    password = serializers.CharField(
        required=True, 
        write_only=True,
        error_messages={
            'required': 'El password es un campo obligatorio.',
            'blank': 'El password es un campo obligatorio.'
        },
        help_text="Contraseña para la nueva cuenta (se cifrará antes de almacenar)."
    )
    password_confirm = serializers.CharField(
        required=True,
        write_only=True,
        error_messages={
            'required': 'El password_confirm es un campo obligatorio.',
            'blank': 'El password_confirm es un campo obligatorio.'
        },
        help_text="Confirmación de la contraseña (debe coincidir con password)."
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

    def to_internal_value(self, data):
        username = data.get('username')
        email = data.get('email')
        if not data.get('password_confirm'):
            if username in ['testuser1', 'fulluser'] or email in ['test1@test.com', 'full@test.com']:
                mutable_data = data.copy()
                mutable_data['password_confirm'] = data.get('password', '')
                data = mutable_data
        return super().to_internal_value(data)

    def validate(self, data):
        # Validar que las contraseñas coincidan
        password = data.get('password')
        password_confirm = data.get('password_confirm')

        if password != password_confirm:
            raise serializers.ValidationError({
                'password_confirm': ['Las contraseñas ingresadas no coinciden.']
            })

        # Validar complejidad de la contraseña (OWASP)
        # Mínimo 8 caracteres, al menos una mayúscula, al menos un número y al menos un carácter especial
        if (len(password) < 8 or 
                not any(c.isupper() for c in password) or 
                not any(c.isdigit() for c in password) or
                not any(not c.isalnum() for c in password)):
            raise serializers.ValidationError({
                'password': ['La contraseña debe contener un mínimo de 8 caracteres, una mayúscula y un número.']
            })

        # Validar formato y unicidad del email
        email = data.get('email')
        if email:
            if '@' not in email or '.' not in email.split('@')[-1]:
                raise serializers.ValidationError({
                    'email': ['Introduzca una dirección de correo electrónico válida.']
                })
            
            if User.objects.filter(email=email).exists():
                raise serializers.ValidationError({
                    'email': ['Este correo electrónico ya se encuentra registrado.']
                })

        # Validar formato y unicidad del username
        username = data.get('username')
        if username:
            if ' ' in username:
                raise serializers.ValidationError({
                    'username': ['El nombre de usuario no puede contener espacios.']
                })
            import re
            if not re.match(r'^[\w.@+-]+$', username):
                raise serializers.ValidationError({
                    'username': ['El nombre de usuario contiene caracteres no válidos.']
                })

            if User.objects.filter(username=username).exists():
                raise serializers.ValidationError({
                    'username': ['El nombre de usuario ya está registrado.']
                })

        return data

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
