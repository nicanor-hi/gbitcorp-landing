# 26 — Inicialización técnica Django + Wagtail (FASE 1.1)

## Alcance y estado

FASE 1.1 completada: se creó la estructura mínima Django/Wagtail, se fijaron dependencias con `uv`, se creó la base de desarrollo indicada y se aplicaron las migraciones estándar. No se implementaron modelos editoriales, homepage, StreamField propio, importador ni frontend público; tampoco se importó contenido ProcessWire.

## Versiones

| Componente | Versión |
|---|---:|
| Python | 3.13.17 (uv gestionado, `.python-version`) |
| uv | 0.13.5 |
| Django | 5.2.18 |
| Wagtail | 7.4.4 (rama LTS 7.4) |
| psycopg | 3.3.6 (`binary`) |
| python-dotenv | 1.2.4 |
| PostgreSQL | 16.1, servicio Windows local, puerto 5432 |

La selección prioriza las ramas LTS compatibles con Python 3.13. Django 5.2 soporta Python 3.13 y PostgreSQL 14+, Wagtail 7.4 LTS admite Django 5.2 y Python 3.13, y Psycopg 3 soporta Python 3.13, Windows y PostgreSQL 16. Fuentes oficiales: [compatibilidad Django](https://docs.djangoproject.com/en/5.2/faq/install/), [notas Django 5.2](https://docs.djangoproject.com/en/5.2/releases/5.2/), [compatibilidad Wagtail 7.4](https://docs.wagtail.org/en/stable-7.4.x/releases/upgrading.html), [instalación Psycopg](https://www.psycopg.org/install/).

## Estructura inicial

```text
manage.py
config/
  __init__.py
  settings/
    __init__.py
    base.py
    local.py
    production.py
  urls.py
  asgi.py
  wsgi.py
templates/
static/
tests/
media/          (generado local, ignorado)
staticfiles/    (generado por collectstatic, ignorado)
```

La configuración instala las apps base de Django/Wagtail necesarias para administración, imágenes/documentos, páginas y redirecciones. `config.urls` publica `/admin/` para Wagtail, `/django-admin/`, `/documents/` y el router Wagtail en `/`. No hay una página inicial pública hasta que una fase futura defina y cree contenido.

## PostgreSQL y límites de administración

- PostgreSQL 16.1 funciona como servicio Windows `pgsql_16.1-1`, tipo Automatic, en `localhost:5432`. El servicio, la configuración y el directorio de datos son administrados por el usuario; Codex no lo inició, detuvo, reinició ni modificó durante esta continuación.
- `C:\pgsql_16.1-1\bin\psql.exe` aparece como archivo de 0 bytes y no ejecutable. No se reemplazó; se utilizó el driver Psycopg del proyecto.
- `.env` incluye un `DATABASE_URL` local. El nombre aleatorio que había en el componente de base fue cambiado localmente a `gbitcorp_wagtail_dev`, preservando credenciales sin imprimirlas. No se incluye URL ni usuario/contraseña en este documento.
- La conexión al servidor confirmó PostgreSQL 16.1. La base objetivo no existía; se creó en UTF-8, propiedad del usuario ya proporcionado. No se crearon roles ni se alteraron permisos. La base contenía 0 tablas/objetos de usuario antes de migrar; luego quedaron 51 tablas no-sistema y 219 migraciones Django/Wagtail aplicadas.
- No se conectó a MySQL histórico ni AWS RDS. No se importó contenido ProcessWire.

## Variables y comandos PowerShell

```powershell
# Desde la raíz del repositorio
$env:PATH = "$env:USERPROFILE\.local\bin;$env:PATH"
uv --version
uv sync
uv run python --version

# .env es local, contiene DATABASE_URL y está ignorado por Git.
# No imprimirlo ni pegarlo en chats, tickets o logs.

uv run python manage.py check
uv run python manage.py makemigrations --check --dry-run
uv run python manage.py migrate
uv run python manage.py test
uv run python manage.py runserver 127.0.0.1:8000
```

Para generar localmente un secreto de desarrollo puede usarse:

```powershell
uv run python -c "import secrets; print(secrets.token_urlsafe(64))"
```

## Settings por entorno

La configuración se separa en `config.settings.base` (común), `config.settings.local` (Windows/desarrollo) y `config.settings.production`.

- `manage.py` usa `config.settings.local` por defecto para facilitar el desarrollo. `local.py` carga `.env`, fija `DEBUG=True`, limita hosts a loopback y deja disponibles los recursos estáticos/media de desarrollo.
- WSGI y ASGI no eligen settings por omisión: el proceso debe definir `DJANGO_SETTINGS_MODULE`. En despliegue, seleccionar explícitamente `config.settings.production`.
- Producción fija `DEBUG=False`, exige `ALLOWED_HOSTS`, activa redirección HTTPS, cookies seguras y cabeceras de proxy (`X-Forwarded-Proto` / `X-Forwarded-Host`). El proxy de confianza debe sobrescribirlas; no usar estas settings con un proxy que permita falsificarlas. HSTS comienza con una hora, sin incluir subdominios ni preload; elevarlo solo tras validar HTTPS en el dominio productivo.
- `manage.py check --deploy` advierte que HSTS no incluye subdominios ni está en preload. Es deliberado hasta confirmar que todos los subdominios usan HTTPS y que el dominio debe entrar en la lista preload; no se silencian esas advertencias.
- `production.py` no carga `.env`. El entorno del despliegue debe proporcionar `SECRET_KEY`, `DATABASE_URL` y `ALLOWED_HOSTS`; configurar `CSRF_TRUSTED_ORIGINS` para los orígenes HTTPS que realmente envíen formularios. `DATABASE_URL` sigue siendo la única configuración PostgreSQL y no se aceptan variables individuales `DB_*`.
- No se fijan rutas de Windows en producción. `STATIC_ROOT` y `MEDIA_ROOT` son rutas bajo `BASE_DIR` por defecto, con `MEDIA_ROOT` configurable mediante variable de entorno; el despliegue/container futuro definirá montajes y servidor de estáticos/media.

Selección local explícita opcional en PowerShell:

```powershell
$env:DJANGO_SETTINGS_MODULE = "config.settings.local"
uv run python manage.py check
```

En despliegue, establecer `DJANGO_SETTINGS_MODULE=config.settings.production` en el entorno del proceso WSGI/ASGI y proporcionar `SECRET_KEY`, `DATABASE_URL` y `ALLOWED_HOSTS` mediante el gestor de secretos/variables del entorno. Añadir `CSRF_TRUSTED_ORIGINS` solo con orígenes HTTPS confirmados. No se proveen valores de producción ni secretos de ejemplo.

Para comandos de gestión productivos, seleccionar `config.settings.production` y cargar las variables mediante el gestor seguro del entorno; no copiar secretos a comandos, archivos versionados ni documentación. No activar `DEBUG` ni usar `runserver` en producción.

El entorno usa `uv` desde `%USERPROFILE%\.local\bin\uv.exe`; si el comando `uv` no está en PATH, invocar esa ruta absoluta o añadir solo esa carpeta al PATH de la sesión PowerShell. No se modifica PATH global ni Python 3.10.

## Migraciones, administración y validación

La conexión se valida sin imprimir la URL. Si falta la base indicada, se permite crear solo esa base en autocommit mediante `psycopg.sql.Identifier`, usando el usuario existente; no crear roles ni cambiar privilegios. Si existe, inspeccionar tablas/objetos y detenerse antes de migrar si hay contenido previo no atribuible al proyecto. Las migraciones solo se ejecutan en el destino confirmado. No se crea superusuario Django automáticamente.

Resultados: `uv sync --locked`, `manage.py check`, `manage.py migrate` y `manage.py migrate --check` pasaron. No hay migraciones propias pendientes (`makemigrations --check --dry-run`: `No changes detected`). Las dos pruebas existentes pasaron. El servidor de desarrollo respondió HTTP 200 en `/admin/login/` y en el CSS de Wagtail, enlazado únicamente a `127.0.0.1`; se detuvo tras validar. No se creó superusuario. No se modificó ni administró el servicio PostgreSQL.

## Pendientes para FASE 1.2

- Crear superusuario de Django solo si se autoriza y con contraseña interactiva segura.
- Diseñar modelos editoriales y StreamField con base en las 49 rutas preservadas y su manifiesto aprobado, nunca importar páginas históricas por defecto.
- La contenerización queda para fases posteriores en Arch Linux y producción; Windows sigue siendo el entorno nativo actual.
- No iniciar frontend ni carga de contenido hasta aprobación de FASE 1.2.
