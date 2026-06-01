from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .serializers import (
    LoginRequestSerializer,
    LoginResponseSerializer,
    RegisterRequestSerializer,
    RegisterResponseSerializer,
    ProfileUpdateSerializer,
    ProfileUpdateResponseSerializer,
    UserDetailSerializer,
    LogoutResponseSerializer
)

@extend_schema(
    summary="Inicio de sesión de usuario",
    description="Recibe credenciales de usuario, las valida y genera/retorna un Token de Django REST Framework junto con los datos del perfil y configuración del usuario.",
    request=LoginRequestSerializer,
    responses={
        200: LoginResponseSerializer,
        400: OpenApiResponse(description="Por favor, proporciona username y password, o usuario desactivado."),
        401: OpenApiResponse(description="Credenciales inválidas.")
    }
)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny]) 
def api_login(request):
    """
    Vista de inicio de sesión.
    Recibe credenciales de usuario, las valida y genera/retorna un Token de Django REST Framework
    junto con los datos del perfil y configuración del usuario.
    """
    username = request.data.get('username')
    password = request.data.get('password')

    # Validación de datos requeridos
    if not username or not password:
        return Response(
            {'error': 'Por favor, proporciona username y password.'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    # Proceso de autenticación
    user = authenticate(username=username, password=password)

    if user is not None:
        if user.is_active:
            # Login clásico para manejo de sesiones opcional
            login(request, user)
            
            # Obtención o creación del Token de DRF para el usuario autenticado
            token, created = Token.objects.get_or_create(user=user)
            
            # Obtener datos de perfil y configuración asociados mediante las señales
            phone = user.profile.phone if hasattr(user, 'profile') else ''
            avatar_url = user.profile.avatar_url if hasattr(user, 'profile') else ''
            
            font_size = user.config.font_size if hasattr(user, 'config') else 'MEDIUM'
            high_contrast = user.config.high_contrast if hasattr(user, 'config') else False
            voice_guidance = user.config.voice_guidance if hasattr(user, 'config') else False
            
            # Respuesta exitosa con el token y datos del usuario
            return Response({
                'message': 'Login exitoso',
                'token': token.key,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'phone': phone,
                    'avatar_url': avatar_url,
                    'config': {
                        'font_size': font_size,
                        'high_contrast': high_contrast,
                        'voice_guidance': voice_guidance
                    }
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Este usuario está desactivado.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        # Credenciales incorrectas
        return Response({'error': 'Credenciales inválidas.'}, status=status.HTTP_401_UNAUTHORIZED)


@extend_schema(
    summary="Registro de usuario",
    description="Recibe username, password, email y opcionalmente teléfono, avatar_url y opciones de accesibilidad. Crea el usuario y sus relaciones (UserProfile, UserConfig), y retorna un Token activo.",
    request=RegisterRequestSerializer,
    responses={
        201: RegisterResponseSerializer,
        400: OpenApiResponse(description="Por favor, proporciona username, password y email, o nombre de usuario / correo ya registrado."),
        500: OpenApiResponse(description="Error al registrar el usuario.")
    }
)
@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def api_register(request):
    """
    Vista de registro de usuario.
    Recibe username, password, email y opcionalmente teléfono, avatar_url y opciones de accesibilidad.
    Crea el usuario y sus relaciones (UserProfile, UserConfig), y retorna un Token activo.
    """
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    
    # Parámetros opcionales del perfil y configuración
    phone = request.data.get('phone', '')
    avatar_url = request.data.get('avatar_url', '')
    font_size = request.data.get('font_size', 'MEDIUM')
    high_contrast = request.data.get('high_contrast', False)
    voice_guidance = request.data.get('voice_guidance', False)
    
    # Validación de campos requeridos
    if not username or not password or not email:
        return Response(
            {'error': 'Por favor, proporciona username, password y email.'},
            status=status.HTTP_400_BAD_REQUEST
        )
        
    # Verificar si el usuario ya existe
    if User.objects.filter(username=username).exists():
        return Response(
            {'error': 'El nombre de usuario ya está registrado.'},
            status=status.HTTP_400_BAD_REQUEST
        )
        
    if User.objects.filter(email=email).exists():
        return Response(
            {'error': 'El correo electrónico ya está registrado.'},
            status=status.HTTP_400_BAD_REQUEST
        )
        
    try:
        # Creación del usuario con la contraseña cifrada
        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password)
        )
        
        # Recuperar y actualizar el perfil creado automáticamente por la señal de Django
        profile = user.profile
        profile.phone = phone
        profile.avatar_url = avatar_url
        profile.save()
        
        # Recuperar y actualizar la configuración creada automáticamente por la señal de Django
        config = user.config
        config.font_size = font_size
        config.high_contrast = high_contrast
        config.voice_guidance = voice_guidance
        config.save()
        
        # Generar Token de autenticación de DRF para el nuevo usuario
        token, created = Token.objects.get_or_create(user=user)
        
        # Respuesta exitosa con el token del usuario recién registrado
        return Response({
            'message': 'Usuario registrado exitosamente',
            'token': token.key,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'phone': profile.phone,
                'avatar_url': profile.avatar_url,
                'config': {
                    'font_size': config.font_size,
                    'high_contrast': config.high_contrast,
                    'voice_guidance': config.voice_guidance
                }
            }
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {'error': f'Error al registrar el usuario: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@extend_schema(
    summary="Cierre de sesión",
    description="Requiere token de autenticación en cabecera y elimina dicho token de la base de datos para invalidar futuros accesos del mismo.",
    responses={
        200: LogoutResponseSerializer,
        500: OpenApiResponse(description="Error al cerrar sesión.")
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_logout(request):
    """
    Vista de cierre de sesión.
    Requiere token de autenticación en cabecera y elimina dicho token de la base de datos
    para invalidar futuros accesos del mismo.
    """
    try:
        # Elimina el token asociado al usuario de manera segura
        request.user.auth_token.delete()
        return Response({'message': 'Sesión cerrada y token eliminado exitosamente.'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': f'Error al cerrar sesión: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@extend_schema(
    methods=['GET'],
    summary="Obtener perfil de usuario logueado",
    description="Obtiene los datos detallados del usuario logueado, incluyendo su perfil y configuración.",
    responses={200: UserDetailSerializer}
)
@extend_schema(
    methods=['PUT', 'PATCH'],
    summary="Actualizar perfil de usuario logueado",
    description="Actualiza el perfil y configuración del usuario logueado (campos como email, teléfono, avatar o configuraciones de accesibilidad).",
    request=ProfileUpdateSerializer,
    responses={
        200: ProfileUpdateResponseSerializer,
        400: OpenApiResponse(description="Error en los campos enviados o conflicto de correo electrónico.")
    }
)
@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def api_profile(request):
    """
    Vista para ver o actualizar el perfil del usuario autenticado.
    Soporta GET, PUT y PATCH. Requiere autenticación por Token.
    """
    user = request.user
    profile = user.profile
    config = user.config

    if request.method == 'GET':
        serializer = UserDetailSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method in ['PUT', 'PATCH']:
        # Validación parcial o completa según el método
        serializer = ProfileUpdateSerializer(data=request.data, partial=(request.method == 'PATCH'))
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        # Actualizar email del usuario si se proporciona
        email = data.get('email')
        if email is not None:
            if email != user.email and User.objects.filter(email=email).exclude(id=user.id).exists():
                return Response({'error': 'El correo electrónico ya está registrado.'}, status=status.HTTP_400_BAD_REQUEST)
            user.email = email
        user.save()

        # Actualizar datos de perfil
        phone = data.get('phone')
        avatar_url = data.get('avatar_url')
        if phone is not None:
            profile.phone = phone
        if avatar_url is not None:
            profile.avatar_url = avatar_url
        profile.save()

        # Actualizar configuración de accesibilidad
        font_size = data.get('font_size')
        high_contrast = data.get('high_contrast')
        voice_guidance = data.get('voice_guidance')

        if font_size is not None:
            config.font_size = font_size
        if high_contrast is not None:
            config.high_contrast = high_contrast
        if voice_guidance is not None:
            config.voice_guidance = voice_guidance
        config.save()

        # Respuesta con el perfil de usuario actualizado
        response_serializer = UserDetailSerializer(user)
        return Response({
            'message': 'Perfil actualizado exitosamente',
            'user': response_serializer.data
        }, status=status.HTTP_200_OK)


@extend_schema(
    summary="Listado de todos los usuarios",
    description="Retorna una lista completa de todos los usuarios registrados, incluyendo su perfil y su configuración de accesibilidad.",
    responses={200: UserDetailSerializer(many=True)}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_users_list(request):
    """
    Vista que devuelve el listado de todos los usuarios registrados.
    Requiere autenticación por Token.
    """
    # select_related optimiza la consulta evitando problemas N+1
    users = User.objects.select_related('profile', 'config').all().order_by('id')
    serializer = UserDetailSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
