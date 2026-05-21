# Proyecto-Final-Electiva-I


# para entrar 

- python -m venv venv
- .\venv\Scripts\Activate.ps1
- pip install -r requirements.txt
- python manage.py migrate
- python manage.py loaddata fixtures/datos_productos.json
- python manage.py runserver

## Despliegue en Render

El proyecto esta preparado para desplegarse en Render usando Django, Gunicorn, WhiteNoise y PostgreSQL.

### Archivos de despliegue

- `render.yaml`: define el servicio web, la base de datos PostgreSQL y las variables de entorno necesarias.
- `build.sh`: instala las dependencias y ejecuta `collectstatic`.
- `.python-version`: fija la version de Python usada por Render.
- `requirements.txt`: contiene las dependencias del proyecto.

### Configuracion de produccion

La aplicacion usa variables de entorno para manejar la configuracion sensible:

- `SECRET_KEY`: clave secreta de Django generada automaticamente por Render.
- `DEBUG`: debe estar en `False` en produccion.
- `DATABASE_URL`: URL de conexion a PostgreSQL, generada desde la base de datos de Render.
- `WEB_CONCURRENCY`: numero de procesos usados por Gunicorn.

Tambien se configuro WhiteNoise para servir archivos estaticos en produccion y `dj-database-url` para conectar Django con PostgreSQL mediante `DATABASE_URL`.

### Comandos usados por Render

Build command:

```bash
bash build.sh
```

Start command:

```bash
bash start.sh
```

### Crear usuario administrador

Como Render puede bloquear la consola Shell en algunos planes, el proyecto incluye el comando `crear_superusuario_render` para crear el administrador automaticamente desde variables de entorno.

En Render se deben crear estas variables:

- `DJANGO_SUPERUSER_USERNAME`: nombre del usuario administrador.
- `DJANGO_SUPERUSER_EMAIL`: correo del administrador.
- `DJANGO_SUPERUSER_PASSWORD`: contrasena del administrador.

El comando usado internamente es:

```bash
python manage.py crear_superusuario_render
```

### Cargar datos iniciales

Si se desea cargar la informacion inicial del inventario:

```bash
python manage.py loaddata fixtures/datos_productos.json
python manage.py crear_roles
```
