from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
@permission_classes([AllowAny]) 
def api_login(request):
    
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response(
            {'error': 'Por favor, proporciona username y password.'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    #Autenticación
    user = authenticate(username=username, password=password)

    if user is not None:
        if user.is_active:
            
            login(request, user)
            return Response({
                'message': 'Login exitoso',
                'user': {
                    'username': user.username,
                    'email': user.email,
                    'id': user.id
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Este usuario está desactivado.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        # Credenciales incorrectas
        return Response({'error': 'Credenciales inválidas.'}, status=status.HTTP_401_UNAUTHORIZED)

