# SmartBooking – Backend (API REST)

API REST del sistema de reservas del espacio de coworking de **SmartBooking Solutions**. La consume la aplicación móvil Android ([smartbooking-app](https://github.com/smartbooking-ivo-konstantinow/smartbooking-app)).

Proyecto del Final Libre del módulo **Programador de Aplicaciones para Móviles** (ISPC).

## Tecnologías

- Python 3.12 o superior · Django 6.1 · Django REST Framework
- Autenticación JWT con djangorestframework-simplejwt (rotación y blacklist)
- MySQL 8.4 en Docker
- Variables de entorno con python-dotenv

## Requisitos previos

- [Git](https://git-scm.com/)
- [Python 3.12 o superior](https://www.python.org/downloads/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/), **abierto** antes de empezar

> **Importante (Windows):** usar una terminal **sin** permisos de administrador. Los archivos creados como administrador generan errores de permisos al trabajar con el usuario normal.

## Instalación paso a paso

Los comandos son para **PowerShell** (Windows). Las variantes para Linux/Mac se indican aparte.

### 1. Clonar el repositorio

```powershell
git clone https://github.com/smartbooking-ivo-konstantinow/smartbooking-backend.git
cd smartbooking-backend
```

### 2. Crear el entorno virtual e instalar las dependencias

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Linux/Mac: `source venv/bin/activate`.

El prompt debe empezar con `(venv)`. Si PowerShell bloquea la activación, ejecutar una vez `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` y repetir.

### 3. Configurar las variables de entorno

Copiar el archivo de ejemplo:

```powershell
Copy-Item .env.example .env
```

Completar en `.env` los valores vacíos:

| Variable | Valor |
|---|---|
| `SECRET_KEY` | Una clave aleatoria. Generarla con el comando de abajo |
| `DB_PASSWORD` | Una contraseña para el usuario de la base |
| `DB_ROOT_PASSWORD` | Otra contraseña, para el usuario root de MySQL |

```powershell
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

Las demás variables (`DB_NAME`, `DB_USER`, `DB_HOST`, `DB_PORT`, `DEBUG`) pueden quedar con los valores del ejemplo. El archivo `.env` está excluido del repositorio y nunca debe subirse.

### 4. Levantar la base de datos

```powershell
docker compose up -d
docker compose ps
```

El contenedor `smartbooking-db` debe figurar como **running**. Esperar unos 20 segundos la primera vez, mientras MySQL se inicializa.

### 5. Crear las tablas

```powershell
python manage.py migrate
```

### 6. Crear los usuarios de demostración

```powershell
python manage.py crear_datos_demo
```

### 7. Iniciar el servidor

```powershell
python manage.py runserver
```

Debe mostrar `Starting development server at http://127.0.0.1:8000/`. Dejar esa terminal abierta.

**Verificación:** en otra terminal, `curl.exe http://127.0.0.1:8000/api/perfil/` debe responder un JSON con `"detail"` (401: el endpoint exige token). Eso confirma que la API funciona.

## Credenciales de demostración

Usuarios de prueba creados por `crear_datos_demo`. **Son de demostración, no reales.**

| Rol | Email | Contraseña |
|---|---|---|
| Administrador | admin@smartbooking.com | Admin#2026 |
| Usuario | prueba@mail.com | Clave#123 |

El Administrador también puede ingresar al panel de Django Admin: http://127.0.0.1:8000/admin/

## Endpoints

| Método | Endpoint | Descripción | Acceso |
|---|---|---|---|
| POST | `/api/auth/register/` | Registro de usuario | Público |
| POST | `/api/auth/login/` | Obtención de access y refresh | Público |
| POST | `/api/auth/refresh/` | Renovación del access (con rotación) | Con refresh |
| POST | `/api/auth/logout/` | Cierre de sesión (blacklist del refresh) | Autenticado |
| GET | `/api/perfil/` | Datos del usuario autenticado | Autenticado |

## Pruebas de la API (Postman)

La colección está en `tests/api/smartbooking.postman_collection.json`.

1. Importarla en Postman.
2. Crear un entorno con la variable `base_url` = `http://127.0.0.1:8000/api` y seleccionarlo.
3. Ejecutar **Login**: los tokens se guardan solos en el entorno para las demás solicitudes.

## Seguridad

- Contraseñas con mínimo 9 caracteres, letras, números y un carácter especial
- JWT: access de 15 minutos, refresh de 1 día, rotación y blacklist
- Permiso por defecto `IsAuthenticated` (cerrado por defecto)
- Secretos en `.env`, fuera del repositorio
- Intentos de login fallidos registrados en `logs/security.log`, sin contraseñas ni tokens

El Plan de Seguridad completo está en la [Wiki del proyecto](https://github.com/smartbooking-ivo-konstantinow/smartbooking-app/wiki/Ciberseguridad).

## Solución de problemas

| Problema | Solución |
|---|---|
| `docker compose` no conecta con Docker | Abrir Docker Desktop y esperar a que diga *Engine running* |
| El puerto 3306 está ocupado | Hay otro MySQL instalado: en `docker-compose.yml` cambiar a `"3307:3306"` y en `.env` poner `DB_PORT=3307` |
| `MySQL 8.4 or later is required` | Usar la imagen `mysql:8.4` del `docker-compose.yml` (no otra versión) |
| `detected dubious ownership` en Git | La carpeta se clonó como administrador: volver a clonarla desde una terminal normal |
| El servidor deja de responder | En Windows, un clic dentro de la terminal la pausa: presionar **Esc** |
