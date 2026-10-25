# 29 — Implementación de modelos Wagtail

**Estado:** FASE 1.2B implementada. Esquema aplicado a la base de desarrollo; no contiene contenido migrado ni páginas editoriales nuevas.

## Resumen

Se implementó la aplicación `editorial` sobre Django 5.2.18 y Wagtail 7.4.4, conforme al contrato de `docs/27_CONTRATO_EDITORIAL_WAGTAIL.md` y las decisiones de `docs/28_RESOLUCION_DECISIONES_EDITORIALES.md`. Los modelos son estructura de administración vacía: la existencia de modelos no cambia el estado `import_authorized=No` de las 49 rutas.

## Aplicación y modelos

La aplicación `editorial` está registrada en `INSTALLED_APPS`; `wagtail.contrib.settings` habilita los settings por sitio. Los modelos registrados son:

| Modelo | Campos propios y relaciones | Uso |
|---|---|---|
| `HomePage` | `hero_copy`; `sections` StreamField | Página única raíz del sitio; composición de secciones confirmadas |
| `BlogIndexPage` | `header_image` → imagen Wagtail | Índice único, bajo el contenedor `/blog/` |
| `BlogPostPage` | `summary`; `body` StreamField; `lead_image`; M2M parental `categories` → `BlogCategory` | Artículos hijos del índice; sin tipos de bloque HTML arbitrario |
| `ServicePage` | `banner_image`; `description`; StreamFields ordenados `content_blocks` y `tools` | Los cuatro slugs públicos bajo sus respectivos ancestros |
| `EulaPage` | `legal_body` RichTextField | Página única bajo `/eula/`; permanece vacía |
| `RouteContainerPage` | Solo columnas heredadas `Page` | Ancestro técnico sin contenido editorial propio |
| `BlogCategory` | `name`, `slug`, `sort_order` | Snippet no navegable, slug único y nombre único sin distinguir mayúsculas |
| `SiteFooterSettings` | `address`, `phone1`, `phone2`, `email_info`, `social_links` | Configuración compartida por sitio; no tiene valores iniciales |

Los campos nativos de Wagtail `Page` (incluidos título, slug, SEO y estado editorial) se conservan. Los campos opcionales de imagen apuntan al modelo de imágenes configurable de Wagtail y no copian archivos.

## Bloques y orden

- `HomePage.sections`: `service_links`, `service_carousel`, `partner`, `about`, `text_section`, `contact_section`. Las listas anidadas conservan orden y agrupación de los repetidores; no incluyen submissions ni configuración de Zoho.
- `BlogPostPage.body`: únicamente `rich_text`, con encabezados H2–H4, énfasis, listas y enlaces. No se definió bloque raw HTML; conversión de HTML ProcessWire queda fuera de esta fase.
- `ServicePage.content_blocks`: `offering` con título, imagen de icono, descripción enriquecida opcional; `tools`: secuencia de imágenes accesibles mediante `ImageBlock`.
- Footer: `social_links` es un StreamField ordenado de registros tipados (título, imagen y URL).
- EULA y descripciones enriquecidas usan un allowlist limitado (`h2`, `h3`, `h4`, negrita, cursiva, listas y enlaces).

## Jerarquía y URLs

`HomePage` solo puede vivir bajo la raíz Wagtail y admite contenedores. Índice y EULA son singleton por tipo; publicaciones solo son hijas del índice; servicios y EULA deben tener el slug y padre del manifiesto. Las restricciones de tipo se expresan con `parent_page_types`, `subpage_types` y validación adicional de ruta.

`RouteContainerPage` limita los siete slugs estructurales del contrato y sus padres. No es creable desde la interfaz, fuerza `show_in_menus=False`, no aporta campos de búsqueda, no emite URL de sitemap y su `serve()` responde 404. Aun así, cuando existan, los ancestros deberán publicarse para resolver las rutas hijas. No se crearon instancias.

Las pruebas construyen únicamente árboles temporales en la base de test, leen del manifiesto las 49 combinaciones de `path`/template y verifican que Wagtail resuelve cada ruta al tipo esperado. También verifican 404 directo para los siete ancestros estructurales, y su exclusión de menú, sitemap y búsqueda. No se crearon las 49 páginas en la base real.

## Migración y base de datos

Se generó `editorial/migrations/0001_initial.py`. La migración inspeccionada contiene exclusivamente operaciones `CreateModel` y restricciones/índices derivados del modelo; no hay carga de datos, SQL manual, `RunPython`, borrados ni alteraciones a modelos existentes.

Antes de aplicarla, Django confirmó la conexión a `gbitcorp_wagtail_dev` en la instancia PostgreSQL local configurada y no encontró tablas `editorial_*`. La base tenía tablas estándar de la inicialización Django/Wagtail. `uv run python manage.py migrate` aplicó `editorial.0001_initial` correctamente; las demás migraciones estándar ya estaban aplicadas. El servicio PostgreSQL no se administró ni modificó.

## Pruebas y validaciones

Resultados registrados al cierre de la fase:

- `uv run python manage.py check`: sin problemas.
- `uv run python manage.py makemigrations editorial`: generó solo `0001_initial`.
- `uv run python manage.py sqlmigrate editorial 0001_initial`: operaciones revisadas, solo creación de esquema.
- `uv run python manage.py migrate`: `editorial.0001_initial` aplicada.
- `uv run python manage.py makemigrations --check --dry-run`: sin cambios pendientes.
- `uv run python manage.py migrate --check`: sin migraciones pendientes.
- `uv run python manage.py test editorial`: 11 pruebas, todas aprobadas.
- Cobertura editorial: modelos sin seeds, tipos de árbol, slugs y relaciones de categorías, bloques permitidos, resolución de las 49 rutas en árbol de prueba y 404 de ancestros.

La suite completa del proyecto (`uv run python manage.py test`) aprobó 13 pruebas en total; `git diff --check` no reportó errores.

## Diferencias, límites y decisiones pendientes

- No se sembraron páginas, contenedores estructurales, categorías, imágenes ni documentos. El sitio Wagtail no puede mostrar contenido público todavía.
- No se impusieron cardinalidades de contenido en blanco para los repetidores: sus filas y orden concretos se cargarán únicamente tras aprobar el manifiesto y los datos.
- Los campos enriquecidos limitan funciones de edición, pero no sustituyen la sanitización de una futura importación. HTML desconocido debe retenerse inerte y revisarse; nunca emitirse con `safe`.
- Títulos/resúmenes ambiguos, asignación de las cinco categorías, selección de assets y EULA requieren revisión editorial/legal. No se resolvieron automáticamente.
- El contrato visual de todos los bloques y las plantillas públicas quedan para una fase frontend posterior. No se implementaron templates ni JavaScript.
- El formulario Zoho solo tiene un bloque editorial de presentación; envío, validación backend, captcha, privacidad y respuestas quedan fuera hasta definir integración.
- `SiteFooterSettings` está registrado pero vacío; no se copiaron datos de contacto ni redes sociales.
- No se creó superusuario ni se verificó una sesión del panel; `manage.py check` confirma registro/configuración Django, no acceso autenticado al admin.

## Siguiente fase

FASE 1.2C deberá definir y aprobar el alcance antes de crear instancias o importar contenido. Recomendación: primero una revisión editorial del manifiesto/valores ambiguos y los medios seleccionados; luego preparar el comando de carga controlada y repetible que cree solo páginas autorizadas, contenedores indispensables, categorías aprobadas y assets confirmados como borradores, con comprobación de URLs y revisión humana antes de publicar. No conectar ni leer la base MySQL como parte automática de la operación sin autorización específica.
