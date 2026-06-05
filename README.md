# API de Mentor Virtual (Backend)

Este repositorio contiene la API REST y el sistema de base de datos para la plataforma **Mentor Virtual**, un servicio de mentoría personalizada y accesible.

---

## 🎯 Visión y Objetivos del Proyecto

El **Mentor Virtual** está diseñado para ofrecer mentoría y guía inteligente a usuarios, con un fuerte enfoque en la **inclusión y accesibilidad**. Apuntamos a:
1. **Accesibilidad Universal**: Permitir que personas con distintas capacidades utilicen la plataforma ajustando tamaños de fuente, contrastes elevados y guía de voz de manera persistente.
2. **Seguridad y Escalabilidad**: Implementar autenticación robusta mediante tokens y dejar sentadas las bases para validaciones avanzadas (como hashing biométrico facial).
3. **Integración Sencilla**: Ofrecer una documentación interactiva completa de la API (OpenAPI 3.0) para simplificar la integración del equipo de Frontend.

---

## 🛠️ Tecnologías Utilizadas

- **Core**: Python 3.12, Django 5.0+ / 6.0+
- **REST API**: Django REST Framework (DRF)
- **Documentación Interactiva**: `drf-spectacular` (Swagger UI & ReDoc)
- **Base de Datos**: PostgreSQL 15 (en Docker) y SQLite3 (fallback local)
- **Contenedores**: Docker & Docker Compose

---

## 💾 Contexto de Memoria para Agentes de IA

> [!NOTE]
> Esta sección permite a otros agentes de IA (como Antigravity, GitHub Copilot, etc.) entender rápidamente la lógica y decisiones del proyecto.

- **Doble Configuración de Base de Datos**: En [settings.py](MentorVirtual/settings.py), la base de datos se configura dinámicamente. Si existe la variable de entorno `DATABASE_URL`, el sistema se conecta a **PostgreSQL** (usado dentro de Docker). Si no está definida, hace fallback a **SQLite3** local (`db.sqlite3`).
- **Señales de Django**: Al crear un nuevo usuario (`User`), se disparan automáticamente señales (`post_save`) que crean y asocian su perfil (`UserProfile`) y su configuración (`UserConfig`). No es necesario crearlos manualmente en las vistas de registro.
- **Autenticación**: Se utiliza `rest_framework.authtoken`. El token se envía en la cabecera HTTP como `Authorization: Token <tu_token>`.

---

## 🚀 Guía de Instalación y Ejecución

### 1. Clonar el Proyecto
```bash
git clone https://github.com/equipo-1-innovalab-2026/equipo1-tm-innova-lab-2026-backend.git
cd equipo1-tm-innova-lab-2026-backend
```

### 2. Levantar con Docker
Asegúrate de tener Docker y Docker Compose corriendo. Ejecuta:
```bash
docker compose up -d --build
```
Esto creará la red del proyecto, el volumen de datos de PostgreSQL y levantará los servicios:
- `db` (PostgreSQL en el puerto `5432`)
- `web` (Servidor Django en el puerto `8000`)

### 3. Ejecutar Migraciones de Base de Datos
Crea las tablas necesarias en la base de datos PostgreSQL ejecutando:
```bash
docker compose exec web python manage.py migrate
```

### 4. Crear un Superusuario (Administrador)
Para acceder al panel de administración de Django, crea un administrador:
```bash
docker compose exec web python manage.py createsuperuser
```
*(Sigue las instrucciones en consola para definir usuario, email y contraseña).*

### 5. Verificar que el Sistema esté Corriendo
Abre tu navegador e ingresa a:
- **Swagger UI**: [http://localhost:8000/api/schema/swagger-ui/](http://localhost:8000/api/schema/swagger-ui/)
- **ReDoc**: [http://localhost:8000/api/schema/redoc/](http://localhost:8000/api/schema/redoc/)
- **Panel de Administración**: [http://localhost:8000/admin/](http://localhost:8000/admin/)

---

## 📁 Estructura del Proyecto

- `/MentorVirtual`: Configuración global de Django (settings, urls, wsgi).
- `/users`: Aplicación de Django que maneja el registro, autenticación, perfiles y configuraciones de accesibilidad.
- `/mentor`: Aplicación dedicada a la lógica futura de mentorías.
- `/documentacion`: Documentación detallada del proyecto.
  - [Endpoints de la API](documentacion/endpoints_guide.md)
  - [Diccionario de Datos](documentacion/data_dictionary.md)
