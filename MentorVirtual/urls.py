"""
URL configuration for MentorVirtual project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from users.views_docs import developer_portal

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/docs/', developer_portal, name='developer_portal'),
    
    # Ruta de la API de usuarios
    path('api/', include('users.urls')), 
    
    # Endpoints para la documentación de la API generada por drf-spectacular
    # Retorna el archivo de especificación OpenAPI en formato YAML/JSON
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    
    # Interfaz interactiva de Swagger UI para probar endpoints
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # Interfaz alternativa premium de Redoc
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

