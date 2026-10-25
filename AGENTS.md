# Instrucciones permanentes para Codex

## Objetivo y estado

Este repositorio reconstruirá el sitio corporativo público `gbitcorp.com`, cuyo CMS actual es ProcessWire, como un proyecto Django + Wagtail con PostgreSQL. Prioridades: conservar identidad, contenidos públicos y URLs verificables; ofrecer edición en Wagtail; mejorar responsive, accesibilidad, seguridad y mantenibilidad.

El trabajo se ejecuta por fases. Las fases 0 (auditoría), 1.1 (base técnica), 1.2B (modelos), 1.2C (validación editorial/administrativa), 2.2A (contratos visuales/editoriales) y 2.2B (Tailwind y layout global) están cerradas. Los modelos editoriales permanecen vacíos; no crear/importar páginas, categorías ni contenido ProcessWire. Las páginas completas y la importación requieren aprobación de sus fases posteriores.

## Alcance y fuentes

- `docs/gbitcorp.com/` es el respaldo original completo de ProcessWire y solo puede inspeccionarse en modo de solo lectura.
- `docs/PLAYWRIGHT_GBITCORP_WAGTAIL.md` es el documento fuente local de configuración de Playwright. Está excluido de Git por contener instrucciones y referencias locales; leerlo antes de usar Playwright.
- Ambos materiales originales son locales y no deben copiarse, modificarse ni subirse al repositorio. Sus exclusiones exactas están en `.gitignore`.
- Existe una restauración local autorizada del dump ProcessWire en `processwire_gbitcorp_local`, en MySQL portable `127.0.0.1:3307`. No conectar a AWS RDS. Toda auditoría debe ser de solo lectura; preferir usuario limitado a `SELECT`/`SHOW VIEW`, nunca consultar campos de password, sesiones, comentarios o mensajes personales, y no escribir valores privados en documentos.
- La preservación del sitio público (49 rutas, capturas y texto) define el alcance migrable. La base es complementaria para resolver datos/dependencias de esas rutas; nunca autoriza importar páginas históricas, templates antiguos ni registros extra por estar presentes o publicados en ProcessWire.
- Las columnas de texto ProcessWire consultadas usan MySQL `latin1` (CP1252) y la sesión de auditoría usa `utf8mb4`; no interpretar esos bytes como ISO-8859-1 ni aplicar conversiones SQL. En los datos públicos se confirmaron signos `?` literales en contenido: no “repararlos” automáticamente; conservar la referencia pública y escalar dudas a revisión editorial.
- Reconciliación confirmada: 74 `blog_images` en 42 artículos públicos y una dependencia adicional del índice `/blog/posts/` (`1037`, `1144-1.jpg`), 75 referencias A en total. La fila restante de las 76 filas globales está fuera del manifiesto y excluida.
- Para la auditoría local existe `pw_auditor@127.0.0.1`, con `SELECT, SHOW VIEW` solo en `processwire_gbitcorp_local` (MySQL portable `127.0.0.1:3307`). No guardar su contraseña. Mantener consultas en allowlist pública/dependencias y no usar `root` para análisis habitual. El permiso del esquema puede leer técnicamente tablas sensibles: no consultar esas tablas/campos.
- No ejecutar otra restauración/dump, ni modificar la DB, ni implementar importador hasta autorización expresa. No inventar contenido, relaciones, formularios o reglas que no puedan corroborarse en la base local, el respaldo de código o el sitio público.
- Mantener como referencia los informes `docs/01_` a `docs/06_`; diferenciar hechos observados, inferencias y pendientes.

## Convenciones de desarrollo

- Inspeccionar primero los archivos indicados por la tarea; limitar cada cambio al módulo relacionado.
- Reutilizar patrones y dependencias existentes. Evitar dependencias y abstracciones nuevas sin necesidad demostrada.
- Preservar URLs existentes o definir redirecciones explícitas; no dejar enlaces internos hacia el CMS antiguo.
- Mantener contenido y bloques administrables en Wagtail. Preferir modelos de página por tipo real observado, StreamField para composición de secciones y snippets/settings solo para elementos compartidos.
- Corregir defectos responsive y de accesibilidad sin copiar esos defectos por fidelidad visual. Auditar especialmente los separadores gráficos hechos con imágenes.
- No hacer cambios a partir de hipótesis sin etiquetarlas como tales.

## Seguridad y datos

- Nunca publicar secretos, credenciales, tokens, cookies, estados de sesión, dumps, archivos de configuración privada o datos de usuarios.
- La copia local de ProcessWire puede contener PII, hashes y contenido histórico. Consultar únicamente metadata/contenido público estrictamente necesario, bajo alcance de solo lectura. No mostrar hashes, correos privados, IP, comentarios ni envíos de formularios.
- No incluir valores sensibles del respaldo ProcessWire en documentación, logs o informes. Describir su existencia y ubicación relativa sin reproducir valores.
- No arrancar ni ejecutar el sitio ProcessWire, PHP antiguo, módulos o scripts del respaldo.
- No enviar formularios reales ni ejecutar acciones que creen registros, mensajes o postulaciones.
- Formularios e integraciones externas requieren confirmar destino y comportamiento; las credenciales nuevas deben manejarse fuera del código y del Git.
- Para probar administración Wagtail, crear usuarios exclusivamente en la base temporal del test runner de Django. Nunca crear superusuarios permanentes en la base de desarrollo sin autorización explícita.

## Seguridad al consultar proyectos de referencia

- Consultar únicamente los archivos necesarios para la tarea; limitar las inspecciones a la configuración o código pertinentes.
- No realizar búsquedas recursivas indiscriminadas que puedan incluir archivos sensibles.
- Excluir expresamente `.env`, `.env.*` con secretos reales, claves privadas, certificados, credenciales y archivos de configuración local sensibles.
- No leer, imprimir, copiar ni registrar secretos de otros proyectos.
- Si se encuentra información sensible accidentalmente, no reproducirla en el reporte ni incorporarla al repositorio.
- Estas restricciones también aplican a herramientas de búsqueda, scripts y comandos ejecutados por agentes automatizados.

## Playwright

- Usar exclusivamente la instalación global ya gestionada por Volta y sus rutas/versiones consignadas en el documento local. No instalar Playwright, Node.js, Volta ni navegadores sin una necesidad nueva y aprobación.
- Antes de automatizar, comprobar la instalación con los comandos documentados en PowerShell.
- Capturar desktop, tablet y móvil; medir desbordamiento horizontal, imágenes fallidas, títulos, enlaces, consola y respuestas HTTP cuando proceda.
- Rastrear solo páginas enlazadas o rutas verificadas en código, sitemap o robots. Registrar origen, href original, clasificación, destino, estado y URL final. No convertir automáticamente subdominios en páginas internas.
- Guardar capturas, HAR y temporales fuera del repositorio, preferiblemente en `C:\Temp\gbitcorp-audit\`. Si un temporal queda dentro del workspace, usar una ruta expresamente ignorada y no incorporarlo a Git.
- No guardar datos privados del navegador ni probar envíos de formulario.

## Entorno Python

- Entorno aislado administrado por uv en `.venv/`, excluido de Git.
- Gestionar Python de este proyecto exclusivamente con Astral `uv`; no crear el entorno con el Python global ni reemplazarlo.
- La versión fijada en `.python-version` es **3.13.17**. `uv` instala su distribución independiente bajo `%APPDATA%\uv\python`; el Python global de Windows no se modifica. `uv` está instalado en `%USERPROFILE%\.local\bin`. El instalador no agregó esa carpeta al PATH de esta sesión; para usar el comando corto en una terminal PowerShell, agregarla solo al PATH temporal de esa sesión (no agregar rutas de Python): `$env:PATH = "$env:USERPROFILE\.local\bin;$env:PATH"`.
- Comandos PowerShell del proyecto:

  ```powershell
  # Si uv aún no está instalado, usar el instalador oficial de Astral:
  powershell -NoProfile -ExecutionPolicy Bypass -Command "irm https://astral.sh/uv/install.ps1 | iex"
  # En esta sesión, exponer solo el ejecutable de uv, no un Python global/gestionado:
  $env:PATH = "$env:USERPROFILE\.local\bin;$env:PATH"
  uv --version
  uv python install 3.13.17 --managed-python
  uv python pin 3.13.17 --managed-python
  uv venv --clear --python 3.13.17 --managed-python .venv
  .\.venv\Scripts\Activate.ps1
  python --version
  python -c "import sys; print(sys.executable); print(sys.prefix != sys.base_prefix)"
  uv pip list --python .venv\Scripts\python.exe
  ```

- `.venv/` está excluido de Git. Antes de recrearlo, inspeccionar `pyvenv.cfg` y paquetes (`uv pip list --python .venv\Scripts\python.exe`) y preservar cualquier dependencia/dato ajeno al entorno. `uv venv --clear` solo se permite para la ruta exacta del `.venv` de este repositorio tras verificarla.
- Para evitar problemas con la política de activación de PowerShell, usar `.\.venv\Scripts\python.exe` directamente y verificar ruta/versión con `.\.venv\Scripts\python.exe --version` y `.\.venv\Scripts\python.exe -c "import sys; print(sys.executable); print(sys.prefix != sys.base_prefix)"`.
- Las dependencias de aplicación se declaran en `pyproject.toml` y se resuelven en `uv.lock`; usar `uv sync` y `uv run`, nunca instalaciones globales. La base técnica actual usa Django 5.2 LTS, Wagtail 7.4 LTS, psycopg 3 y Python 3.13.17; revisar compatibilidad oficial antes de actualizar.
- Settings separados en `config/settings/base.py`, `local.py` y `production.py`. `manage.py` puede usar local como predeterminado; WSGI/ASGI requieren `DJANGO_SETTINGS_MODULE` explícito. Producción debe seleccionar `config.settings.production` con `DEBUG=False` y `ALLOWED_HOSTS` explícitos. Configuración local carga `.env` ignorado; producción recibe variables desde el entorno del despliegue y no carga `.env` automáticamente.
- `.env.example` no lleva secretos. `DATABASE_URL` es la única fuente de configuración PostgreSQL; si falta o es inválida, Django debe fallar explícitamente. No usar variables individuales `DB_*`. No incluir credenciales en código, argumentos, documentación ni Git.
- La configuración de producción asume un reverse proxy de confianza que sobrescribe `X-Forwarded-Proto` y `X-Forwarded-Host`; validar esa configuración en el entorno real antes de desplegar. HTTPS seguro no se aplica en settings locales.
- PostgreSQL es un servicio administrado por el usuario. Codex no debe iniciarlo, detenerlo, reiniciarlo, deshabilitarlo, reinstalarlo ni modificar servicio, configuración o datos del servidor. Solo conectar a la instancia local indicada por `.env`. Si la base de `DATABASE_URL` no existe, se permite crear únicamente esa base con el usuario existente, autocommit e identificador escapado con psycopg; no crear roles ni cambiar privilegios. Si ya existe, inspeccionar objetos antes de migrar y detenerse si hay tablas/datos previos no atribuibles al proyecto. Aplicar migraciones solo a la base confirmada.
- El desarrollo actual es nativo en Windows; la contenerización se planifica posteriormente para Arch Linux y producción.
- Ejecutar `manage.py runserver` solo enlazado a `127.0.0.1`; no exponer el servidor de desarrollo a la red.
- Modelos editoriales vigentes: app `editorial`; contrato en `docs/27_` y `docs/28_`, implementación en `editorial/models.py` y bloques en `editorial/blocks.py`. La app define estructura vacía solamente. La preservación pública y manifiesto de 49 rutas fijan alcance; las 762 páginas históricas y 728 assets de ProcessWire no son importables en bloque.
- La base PostgreSQL de desarrollo contiene el esquema editorial de FASE 1.2B; solo aplicar migraciones autorizadas a `gbitcorp_wagtail_dev`. No administrar el servicio PostgreSQL ni cambiar usuarios/privilegios. No ejecutar migraciones hacia otras bases.
- `RouteContainerPage` son ancestros técnicos, no contenido: deben permanecer fuera de menús, búsqueda y sitemap, devolver 404 directamente y solo existir para resolver rutas hijas verificadas. No crear sus instancias automáticamente sin autorización de la fase de carga de estructura/contenido.
- No crear/importar las 49 páginas ni sus dependencias, categorías o medios hasta autorización explícita. Todas siguen `import_authorized=No`; modelos vacíos no constituyen aprobación editorial.
- No renderizar HTML heredado de ProcessWire como seguro. `BlogPostPage.body` admite RichText acotado e imágenes mediante `ArticleImageBlock` tipado; contenido fuente no representable requiere staging inerte, allowlist/sanitización y revisión. Las tablas históricas no se convierten automáticamente; EULA permanece vacío hasta aprobación legal/editorial.
- Formularios Zoho son integración funcional fuera de los modelos editoriales; no copiar configuraciones heredadas, credenciales ni enviar solicitudes.

## Frontend global

- El frontend usa Django Templates y Tailwind CSS v4 mediante `@tailwindcss/cli`; no usar CDN, framework SPA ni Bootstrap. Usar Volta con Node.js 22.13.0; npm 10.9.2 fue verificado como funcional en el diagnóstico previo. Ejecutar npm preferentemente mediante `volta run --node 22.13.0 npm ...`: `volta run --node 22.13.0 npm --version`, `volta run --node 22.13.0 npm ci`, `volta run --node 22.13.0 npm run build` y `volta run --node 22.13.0 npm run dev`. En PowerShell, npm puede resolverse como `npm.ps1` y fallar al localizar `npm-prefix.js`; no interpretar ese síntoma como instalación dañada ni reinstalar Node, npm o Volta. No cambiar la configuración global de PowerShell ni sus políticas de ejecución para corregirlo. Los scripts deben existir en `package.json`. Dependencias exactas en `package.json`/`package-lock.json`; `node_modules/` y `static/css/site.css` son generados e ignorados. El build debe ocurrir antes de `collectstatic`/despliegue; Node no se necesita durante las peticiones HTTP.
- Tailwind parte de `static/src/css/site.css`; las fuentes se limitan a `templates/` y `static/js/`. Mantener clases completas/estáticas y no escanear `docs/`, ProcessWire, `docs/reference/` ni valores editoriales arbitrarios.

## Validación y documentación

- Antes de implementar, aclarar impacto en URLs, modelos, migraciones, datos, permisos, seguridad, integraciones y pruebas.
- Validar primero el módulo afectado y ampliar la comprobación según riesgo. No declarar verificada una ruta o comportamiento que no se haya probado.
- Revisar el diff y confirmar que solo incluya archivos del alcance y que no exponga secretos.
- Mantener informes concisos, reproducibles y basados en evidencia; conservar inventarios extensos en formatos legibles por máquina cuando resulte útil.
- Registrar limitaciones debidas a MySQL, certificados, acceso a servicios externos o permisos locales.

## Git

- No ejecutar `git add .`, `git add -A`, commit o push salvo solicitud expresa del usuario.
- Antes de cualquier operación de Git sobre materiales originales, comprobar sus rutas, exclusiones y estado de rastreo. Si estuvieran rastreados, detenerse y comunicarlo antes de tocar el índice.
- No eliminar, alterar ni mover los materiales originales.
- No modificar ni incluir archivos personales o cambios preexistentes fuera de alcance.
