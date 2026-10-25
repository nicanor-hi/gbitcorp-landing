# Contexto del proyecto gbitcorp-landing

## Objetivo

Migrar el sitio corporativo público `https://gbitcorp.com` de ProcessWire a Django + Wagtail y PostgreSQL. La prioridad es reconstruir con alta fidelidad lo comprobado públicamente y en los archivos locales, con mejor comportamiento responsive y administración de contenido en Wagtail.

## Estado de fase

Fases 0 a 0.6.1 (auditoría y preservación) completadas y publicadas en `102a0bf`. FASE 1.1 completada: estructura Django/Wagtail, dependencias bloqueadas, configuración por `.env`, base PostgreSQL de desarrollo y migraciones estándar verificadas. FASE 1.2B completada: modelos editoriales vacíos, StreamFields, snippet de categorías y migración de esquema aplicados. FASE 1.2C completada: 16 pruebas pasan, las 49 rutas del manifiesto resuelven en fixtures temporales y la administración fue validada con usuario efímero de test. FASE 2.2A.3 completada: `HomePage.hero_image` opcional y bloque tipado de imagen en artículos; migración aplicada y 17 pruebas pasan. No se crearon páginas, categorías, assets ni contenido migrado en la base permanente; las 49 rutas siguen con `import_authorized=No`. No hay frontend público. Ver `docs/30_VALIDACION_EDITORIAL_WAGTAIL.md` y `docs/35_AJUSTES_EDITORIALES_FRONTEND.md`.

## Hechos observados

- Respaldo local en `docs/gbitcorp.com/`, excluido de Git. El core declara ProcessWire **3.0.229** (`wire/core/ProcessWire.php`).
- El respaldo contiene `wire/` (core), `site/templates/`, `site/modules/` y `site/assets/`; el conteo local fue de 3,786 archivos.
- `site/templates/` tiene 44 archivos PHP y recursos CSS, JS, imágenes, SVG, iconos y fuentes. Hay carpetas `old` y `old2` que necesitan revisión de uso antes de migrar.
- Se contaron 728 archivos en `site/assets/files/`. FASE 0.6.1 concilió `blog_images`: 74 referencias en 42 artículos + 1 en el índice público `/blog/posts/` (ID 1037, archivo `1144-1.jpg`, usado como fondo del encabezado) = 75 medios `blog_images` A locales. La tabla tiene 76 filas; una queda fuera del manifiesto público. Sumadas 83 referencias `icon` y 14 `image`, hay 172 referencias de medios A locales; esto no mapea ni aprueba todo el directorio.
- Se observaron módulos locales de formularios, blog, suscripción, programación de páginas, correo SMTP y compartición social, junto con módulos de terceros. Ver `docs/01_AUDITORIA_PROCESSWIRE.md`.
- Se preservaron 49 páginas públicas HTTP 200 a través de 51 destinos internos únicos intentados; dos variantes `www.gbitcorp.com` fallaron antes de navegación por error de certificado. En las páginas se encontraron 1,645 apariciones de enlaces: 992 internos, 414 externos y 239 especiales. No se navegó a destinos externos. `robots.txt` y `sitemap.xml` devolvieron 404.
- `docs/reference/` contiene 351 PNG (49 páginas × 7 viewports y 8 capturas de interacción), junto a texto visible completo, metadatos/estructura por página, manifest, CSV de enlaces, recursos y mediciones responsive. Resoluciones: 1920×1080, 1440×900, 1366×768, 1024×768, 768×1024, 390×844 y 375×812. La cobertura y excepciones se detallan en `docs/07_PRESERVACION_SITIO.md`.
- Mediciones de scroll horizontal: 0/49 páginas en 1920, 1440 y 1366; 3/49 a 1024; 10/49 a 768; 18/49 a 390 y 375. Hay casos de imágenes/tablas de ancho fijo y contenido editorial desbordado; ver `docs/12_PROBLEMAS_RESPONSIVE.md`.
- En auditoría puntual adicional del Home, las vueltas dieron `loadEventEnd` terminado de 12.8–18.3 s (una captura móvil quedó todavía pendiente) frente a HTML recibido en 0.59–0.65 s, en headless sin throttling; mobile `DOMContentLoaded` + 1.2 s mostró el fondo del hero aún sin pintar. Se guardaron capturas inicial/completa en desktop/tablet/móvil y telemetría sin query strings en `docs/reference/home/`; ver `docs/14_DIAGNOSTICO_HOME_RENDIMIENTO.md`. El fondo de ciudad pesa 5.05 MB; hay fondos `cover` de proporciones muy distintas a las secciones y fotografías/carrusel de 1.5–2.1 MB. Causa/tiempos por recurso pueden variar por red y servicios terceros.
- La inspección visual nueva detectó espacio vertical excesivo bajo las tarjetas del blog en tablet/móvil; `.blog` conserva altura fija de 1440 px en CSS móvil. El detalle y el estado completo están en el diagnóstico Home.
- La portada incluye un formulario que envía a Zoho CRM; no se envió. Su destino y campos deben revisarse funcionalmente antes de reconstruir.
- Se restauró localmente el dump autorizado en `processwire_gbitcorp_local`, en MySQL portable `127.0.0.1:3307`. Auditoría read-only confirmó servidor 8.4.4; el encabezado del dump declara origen MariaDB 10.11.16. No conectarse a RDS ni repetir dump/restauración. La copia contiene datos potencialmente sensibles; no consultar ni migrar valores de usuarios, hashes, sesiones, comentarios o formularios.
- Esquema confirmado: 80 tablas (68 `field_*`), 762 páginas, 53 templates, 67 fields, 56 fieldgroups y 174 asociaciones fieldgroup-field. Todas InnoDB y collation `latin1_swedish_ci`, frente al default utf8mb4 de base; no hay FK declaradas. Las 49 rutas públicas HTTP 200 tienen match exacto en la base. Ver `docs/15_`–`docs/19_`.
- **Prioridad de contenido:** las 49 rutas preservadas en el sitio público fijan el alcance. MySQL solo complementa sus campos/relaciones/assets; no habilita importar páginas históricas o registros adicionales. `pw_auditor@127.0.0.1` tiene `SELECT, SHOW VIEW` solo sobre la base local; no se usó `root` ni RDS. Las 49 rutas tienen match de ID, jerarquía y template en SQL. Los 48 títulos cuyo template consume el título DB coinciden con la referencia pública tras normalizar espacios/sufijo de marca; la página 1086 usa `blog_body` para el H2 visible y su H4 `$page->title` está comentado. EULA toma texto de `eula.php` estático.
- Charset confirmado: `field_title.data`, `field_resume.data`, `field_blog_body.data` son `latin1`; la sesión es `utf8mb4`. La decodificación CP1252 coincide con la conversión MySQL a UTF-8 en 49/49 títulos, 42/42 resúmenes y 42/42 cuerpos. No hubo marcadores comunes de mojibake ni U+FFFD. Se detectaron signos `?` literales almacenados (8 cuerpos, 7 resúmenes), también visibles en contenido preservado; no intentar restaurar letras por heurística. Algunos resúmenes no tuvieron coincidencia exacta de extracción y requieren revisión editorial; ver `docs/20_`.
- Dependencias B confirmadas: 10 repetidores de Home, 19 elementos `content` y 64 `tools` en las cuatro páginas de servicio, cinco categorías relacionadas y visibles en filtros, y 172 referencias de medios (75 `blog_images`, 83 `icon`, 14 `image`), todas con coincidencia local. Los 191 targets únicos de tags no se ven en los templates públicos inspeccionados y quedan C/excluidos; también se excluyen nueve servicios adicionales no preservados.
- La auditoría consultó solo páginas A y dependencias necesarias; no se consultaron valores sensibles ni campos privados. La cuenta tiene permisos de lectura de esquema, por lo que sigue siendo obligatoria la disciplina de consultas acotadas.

## Entorno y dependencias

- Windows y PowerShell.
- Python del proyecto gestionado por uv: **CPython 3.13.17**, fijado en `.python-version`. Intérprete administrado: `%APPDATA%\uv\python\cpython-3.13.17-windows-x86_64-none\python.exe`. `uv` **0.13.5** está instalado en `%USERPROFILE%\.local\bin` mediante el instalador oficial de Astral.
- `.venv/` fue creado con Python uv gestionado 3.13.17; `pyvenv.cfg` apunta a esa distribución y `sys.prefix != sys.base_prefix`. Ahora contiene las dependencias Django/Wagtail definidas en `uv.lock`; `.venv/` sigue excluido de Git.
- Python global de Windows permanece intacto e independiente: `C:\Users\nican\AppData\Local\Programs\Python\Python310\python.exe`, versión 3.10.5. El comando global `python` sigue resolviendo a esa instalación; no se añadió Python 3.13 al PATH ni se cambió el ejecutable global.
- Playwright global 1.61.1 por Volta con Chromium 1228. El documento local fue leído íntegramente y sus instrucciones respetadas.
- Versiones bloqueadas en `uv.lock`: Django **5.2.18**, Wagtail **7.4.4**, psycopg **3.3.6** con extra binary y python-dotenv; todas estables en el momento de la selección. Django 5.2 y Wagtail 7.4 son ramas LTS compatibles con Python 3.13 y PostgreSQL 16. No instalar paquetes globalmente.

## FASE 1.1 — Inicialización Django/Wagtail

- Estructura base: `manage.py`, `config/` (settings, URLs, WSGI, ASGI), `templates/` y `static/`. No se crearon apps editoriales ni modelos propios. Las URLs iniciales exponen `/admin/`, `/django-admin/`, `/documents/` y el enrutador Wagtail en `/`; no hay homepage pública todavía.
- Settings separados: `config.settings.base` (común), `config.settings.local` (carga `.env`, DEBUG y hosts loopback) y `config.settings.production` (DEBUG apagado, hosts explícitos y controles HTTPS). `manage.py` predetermina local; WSGI/ASGI requieren selección explícita por `DJANGO_SETTINGS_MODULE`. Producción no carga `.env` automáticamente.
- `DATABASE_URL` es la única configuración admitida para PostgreSQL; si falta o es inválida, Django falla explícitamente. `.env.example` contiene placeholders; `.env`, media, staticfiles, cache y SQLite están ignorados. Producción debe proporcionar `SECRET_KEY`, `DATABASE_URL`, `ALLOWED_HOSTS` y, según el dominio, `CSRF_TRUSTED_ORIGINS`; el reverse proxy debe sobrescribir las cabeceras forward configuradas.
- PostgreSQL 16.1 se ejecuta como servicio Windows `pgsql_16.1-1`, automático y administrado por el usuario, en localhost:5432. Durante FASE 1.1 solo se consultó su estado; no se controló ni modificó el servicio/configuración. `bin/psql.exe` en la instalación referida tiene tamaño 0 bytes; no se reemplazó. Las comprobaciones/operaciones de esta fase utilizaron psycopg desde el entorno del proyecto.
- El archivo `.env` local (ignorado) contiene `SECRET_KEY` aleatoria y `DATABASE_URL`; el marcador de nombre aleatorio fue sustituido localmente por `gbitcorp_wagtail_dev`. No se documenta la URL ni credenciales. La base inexistente se creó en UTF-8 con el usuario ya proporcionado como propietario; no se crearon roles ni se alteraron privilegios. Hay 51 tablas no-sistema y 219 migraciones estándar aplicadas.
- `manage.py check`, `migrate --check`, `uv sync --locked` y dos pruebas sin DB pasaron. `/admin/login/` y el CSS estático Wagtail devolvieron HTTP 200 desde el servidor de desarrollo enlazado a `127.0.0.1`; no se creó superusuario. El proceso de desarrollo se cerró tras las pruebas.
- Windows es el entorno nativo de desarrollo. No se utilizó Docker; la contenerización se reserva para fases posteriores en Arch Linux y producción. No se usó MySQL histórico ni RDS. La base ProcessWire permanece fuera de esta fase.

## FASE 1.2B — Modelos editoriales Wagtail

- App `editorial` con `HomePage`, `BlogIndexPage`, `BlogPostPage`, `ServicePage`, `EulaPage`, `RouteContainerPage`, `BlogCategory` snippet y `SiteFooterSettings`.
- Siete rutas estructurales están expresadas por validaciones del tipo `RouteContainerPage`; no se crearon instancias. Sus rutas directas responden 404, no aparecen en menú/sitemap y el tipo no ofrece creación desde el editor.
- Home tiene StreamField tipado para las secciones auditadas y copy de hero; BlogPost usa StreamField con solo un bloque RichText limitado, categorías M2M; ServicePage usa bloques ordenados de ofertas e imágenes de herramientas; EULA utiliza RichTextField con allowlist. Ajustes compartidos de footer/social son settings por sitio.
- Migración `editorial.0001_initial` aplicada a `gbitcorp_wagtail_dev` tras confirmar que solo existía el esquema base; crea tablas editoriales sin contenido. El servicio PostgreSQL lo administra el usuario y no fue alterado.
- 11 pruebas editoriales verifican ausencia de seeds, jerarquías, slugs/categorías, StreamField, resolución de las 49 rutas del manifiesto en árbol de prueba y 404 de los siete ancestros. Véase `docs/29_IMPLEMENTACION_MODELOS_WAGTAIL.md`.
- La implementación de modelos no autoriza importar ni publicar contenido. Aprobación editorial de páginas/categorías/media y aprobación legal de EULA siguen pendientes. Zoho/frontend quedan fuera de esta fase.

## FASE 1.2C — Validación editorial y administrativa

- 16 pruebas automatizadas pasan. El test runner usa su base temporal para árbol de 56 nodos (49 rutas públicas y siete ancestros), usuario de administración temporal, relaciones y medios temporales; no se pobló la base de desarrollo.
- La administración de páginas, snippet y settings se verificó con cliente Django: anónimo redirige a autenticación y sesión efímera autorizada obtiene 200. La validación de rutas es resolución Wagtail, no renderizado del frontend.
- `manage.py check`, `makemigrations --check --dry-run`, `migrate --check` y `git diff --check` pasan. Settings de producción se importaron con variables ficticias, sin conexión a producción. No se generaron migraciones nuevas.
- RichText limitado no constituye sanitización del HTML legado. El futuro importador requiere allowlist y revisión; no usar `StreamField.to_python` como validador de bloques desconocidos, pues el comportamiento del framework puede omitir tipos desconocidos.
- Detalle: `docs/30_VALIDACION_EDITORIAL_WAGTAIL.md`. FASE 1.2C no autoriza importar contenido ni construir frontend.

## FASE 2.2A.3 — Ajustes editoriales previos al frontend

- `HomePage.hero_image` es FK opcional al modelo de imágenes Wagtail con `SET_NULL`; no se asignó una imagen por defecto. La ausencia debe tratarse como estado normal en el futuro template.
- `BlogPostPage.body` conserva el bloque `rich_text` existente y agrega `image` (`ArticleImageBlock`): chooser nativo Wagtail, texto alternativo obligatorio salvo marcado decorativo, leyenda opcional y alineación vacía/izquierda/derecha. Izquierda/derecha se apoyan en las clases observadas en el HTML público; no se generaron alt ni se importaron medios.
- `editorial.0002_homepage_hero_image_alter_blogpostpage_body` contiene solo el nuevo campo opcional y un `AlterField` de StreamField sin operación SQL de datos; se aplicó a `gbitcorp_wagtail_dev`.
- Las doce tablas históricas siguen sin conversión: ocho envolturas de maquetación, dos comparativas PWA pendientes de revisión de encabezados y dos casos Cloud ambiguos. Cualquier conversión debe conservar contenido y detenerse ante datos no representables; ver `docs/34_CLASIFICACION_TABLAS_ARTICULOS.md` y `docs/35_AJUSTES_EDITORIALES_FRONTEND.md`.
- No se crearon páginas/categorías ni se importaron imágenes. Las 49 rutas siguen siendo el único alcance público, pero importación/publicación continúa sin autorización. No se cambió ningún modelo de carrusel ni se inició frontend.

## Arquitectura objetivo (propuesta, no implementada)

- Django con PostgreSQL y Wagtail para edición.
- Modelos de página basados en tipos reales encontrados: portada, páginas de servicios/negocio, listados y artículos del blog, páginas informativas y licencia/EULA si continúa vigente.
- StreamField para secciones de composición variable y editables; definir bloques después de revisar todas las plantillas y páginas verificadas.
- Imágenes y documentos administrados por Wagtail. Snippets/settings para navegación, footer y datos corporativos compartidos si el modelo de contenido lo confirma.
- Formularios implementados con validación, protección contra abuso, almacenamiento mínimo y destino de integración explícito; no trasladar configuración SMTP/Zoho antigua ni secretos.
- Mapa de URL con conservación de slugs y redirecciones 301 solo cuando sean necesarias y verificadas.

## Decisiones y límites

- No usar ni modificar el proyecto original; no versionar el respaldo ProcessWire ni el documento fuente de Playwright.
- No instalar dependencias Django/Wagtail en Fase 0.
- Las páginas protegidas, no enlazadas, privadas o dependientes de datos MySQL no se inventan ni se publican automáticamente.
- La preservación pública es la fuente principal del alcance migrable; la base ProcessWire es complementaria y no autoriza ampliar el contenido.
- Las mejoras responsive pueden reemplazar divisores de imagen por CSS/SVG responsive, preservando intención visual.
- Ver la auditoría inicial en `docs/01_AUDITORIA_PROCESSWIRE.md` a `docs/06_PLAN_MIGRACION.md`, preservación en `docs/07_PRESERVACION_SITIO.md` a `docs/14_DIAGNOSTICO_HOME_RENDIMIENTO.md`, y auditoría/modelo/mapeo DB en `docs/15_AUDITORIA_MYSQL_PROCESSWIRE.md` a `docs/19_ESTRATEGIA_IMPORTACION.md`.
- FASE 0.5–0.6.1 documenta codificación, manifiesto de 49 rutas, clasificación editorial, assets, preparación del importador y cierre en `docs/20_` a `docs/25_`; el CSV `docs/21_MANIFIESTO_CONTENIDO_VIGENTE.csv` sigue siendo una allowlist candidata, no aprobación de publicación.
- La implementación Django/Wagtail de FASE 1.1 se limita a configuración técnica base y migraciones estándar. El usuario administra el servicio PostgreSQL; Codex no lo controla. La base autorizada para desarrollo es `gbitcorp_wagtail_dev`; no se creó usuario ni se cambiaron privilegios. No se crea superusuario sin autorización expresa.
- FASE 1.2B incorpora únicamente esquema editorial vacío según `docs/27_CONTRATO_EDITORIAL_WAGTAIL.md` y `docs/28_RESOLUCION_DECISIONES_EDITORIALES.md`. El manifiesto es allowlist candidata, no autorización; no sembrar las 49 páginas, los siete ancestros, cinco categorías ni medios automáticamente. Consultar el informe `docs/29_IMPLEMENTACION_MODELOS_WAGTAIL.md`.
- El respaldo ProcessWire y el documento fuente Playwright permanecen locales e ignorados. Las referencias de assets apuntan a las rutas del respaldo; no se copiaron assets binarios a `docs/reference/`, por lo que estas referencias no son autosuficientes si se pierde el respaldo local. No se modificó el original.
