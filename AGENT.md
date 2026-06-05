# Agent System Prompt - Mentor Virtual Backend

Este archivo sirve como memoria persistente y guía de contexto de desarrollo para cualquier Agente de IA que trabaje en este proyecto.

---

## 🎯 Información del Proyecto
**Mentor Virtual** es una plataforma de mentoría accesible e inclusiva.
- **Rama activa principal**: `feature/login-improvements`
- **Enfoque técnico**: Backend REST API accesible, integrado con Docker y PostgreSQL.

---

## 🛠️ Stack Tecnológico
- **Lenguaje**: Python 3.12
- **Framework**: Django 5.0+ / 6.0+ & Django REST Framework (DRF)
- **Base de Datos**: PostgreSQL 15 (Docker) / SQLite3 (Fallback local)
- **Documentación**: OpenAPI 3.0 / Swagger UI (vía `drf-spectacular`)
- **Contenedores**: Docker & Docker Compose

---

## 💾 Contexto Crítico & Reglas de Desarrollo

### 1. Base de Datos Dinámica
En [settings.py](MentorVirtual/settings.py), la conexión a la base de datos se resuelve dinámicamente:
- Si `DATABASE_URL` está definida en el entorno, se parsea usando `urllib.parse` para conectarse a **PostgreSQL**.
- Si no está definida, hace fallback a **SQLite3** (`db.sqlite3`).
- *Cualquier cambio de dependencias debe reflejarse en `requirements.txt`.*

### 2. Señales Automáticas (Django Signals)
El modelo `User` está enlazado a `UserProfile` y `UserConfig` mediante señales en `users/models.py`.
- **Acción**: Al crear un `User`, se disparan las señales `post_save` creando el perfil y la configuración correspondientes.
- **Regla**: **No** instanciar `UserProfile` ni `UserConfig` manualmente durante el registro en las vistas; Django lo hace automáticamente.

### 3. Rutas y Documentación
Toda la documentación interactiva está configurada bajo el path `/api/schema/`:
- **Swagger UI**: `/api/schema/swagger-ui/`
- **ReDoc**: `/api/schema/redoc/`
- **Esquema YAML**: `/api/schema/`

---

## 🗃️ Diccionario de Datos Rápido

- **`auth_user`**: Almacena credenciales de usuario (id, username, password, email, is_active).
- **`users_userprofile`**: Datos del perfil (id, user_id [FK 1:1], phone, avatar_url).
- **`users_userconfig`**: Preferencias de accesibilidad (id, user_id [FK 1:1], font_size ['SMALL', 'MEDIUM', 'LARGE'], high_contrast [bool], voice_guidance [bool]).
- **`authtoken_token`**: Tokens de sesión de DRF (key, user_id [FK 1:1], created).

---

## 🚀 Comandos Útiles

- **Iniciar entorno**: `docker compose up -d --build`
- **Ver logs**: `docker compose logs -f web`
- **Migraciones**: `docker compose exec web python manage.py migrate`
- **Crear Superusuario**: `docker compose exec -e DJANGO_SUPERUSER_PASSWORD=<pass> web python manage.py createsuperuser --username <user> --email <email> --no-input`

---

## 📂 Estructura del Proyecto
- `/MentorVirtual`: Configuración del proyecto Django.
- `/users`: Gestión de autenticación, perfiles y accesibilidad.
- `/mentor`: Lógica futura de mentorías.
- `/documentacion`: Guías de la API y modelos de datos.
