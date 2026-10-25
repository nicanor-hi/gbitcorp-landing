# 13 — Mapeo ProcessWire a Wagtail

El mapeo describe candidatos basados en archivos y rutas observados. La relación exacta de páginas ProcessWire con templates/campos reside en MySQL y no está disponible; por ello, todo mapeo salvo el explícito por código se marca como inferencia.

| Página/componente observado | Candidato ProcessWire | Confianza / evidencia | Representación Wagtail sugerida |
|---|---|---|---|
| `/` portada | `site/templates/home.php`; header/footer compartidos en `header.php`/`footer.php` | Alta: la plantilla `home.php` contiene estructura/recursos de la portada | `HomePage` y StreamField para hero, líneas, servicios, partners, equipo, clientes, esencia, artículos y contacto. Snippets/settings para header/footer si se confirma edición global. |
| `/blog/posts/` listado | `blog-posts.php`, con layouts parciales `blog-main.inc`/`blog-side-bar.inc` | Media: coincidencia de ruta, nombres y estructura; asignación de template no comprobable sin MySQL | `BlogIndexPage`, bloques/características reutilizables, paginación y filtros solo si se confirman. |
| `/blog/posts/<slug>/` artículos | `blog-post.php`, parciales y componentes de comentarios/tags | Media: coincide la familia de rutas y plantillas disponibles | `BlogPostPage` con fecha, imagen, cuerpo StreamField, SEO y términos solo cuando el contenido real se confirme. |
| `/negocio/.../` páginas de servicio | `service.php`, `service_service.php`, `business_model.php` y archivos de servicios relacionados | Baja/media: candidatos derivados de nombres y contenido; el template aplicado no está expuesto | `BusinessPage`/`ServicePage` según diferencias reales del contenido; preservar cada URL y CTA. |
| `/eula/quickbook/` | `eula.php` | Media: coincidencia de ruta/nombre; confirmar texto y vigencia con propietario | `StandardPage` o página legal tipada; conservar URL si continúa vigente. |
| Header, navegación, footer | `header.php`, `footer.php`; existen `header_old.php`/`footer_old.php` | Alta para variantes actuales observables; las versiones antiguas no se migran sin uso demostrado | Navegación editable con snippet/settings o páginas referenciadas; footer global con datos validados. |
| Fondos, logo e ilustraciones | `site/templates/img/new/**`; hojas `css/new/**` | Alta en referencias de recursos que coinciden con archivos locales | Imágenes Wagtail si deben editarse; formas decorativas reemplazables por CSS/SVG responsive. |
| Fotografías, miniaturas y logos de contenido | `site/assets/files/<id>/...` | Alta para archivo encontrado, baja para su asociación editorial (depende MySQL) | Importar a Wagtail Images tras confirmar página, nombre, alt, focal point y licencia. |
| Navegación/blog/animación | `site/templates/scripts/main.js`, `blog.js`; `js/new/**` | Media/alta por URL de recursos cargados en páginas públicas | Reimplementar interacciones puntuales en frontend nuevo; no copiar librerías viejas sin justificación. |
| Formulario contacto | La portada contiene HTML Zoho; módulo local `SimpleContactForm` también existe | Alta para acción pública Zoho; el estado/uso del módulo local no está confirmado | Formulario Django/Wagtail con validación y antispam; integración CRM solo tras confirmar requisitos/entorno sandbox. |

## Recursos y trazabilidad

`docs/reference/assets.csv` contiene página, tipo de recurso, URL, ruta coincidente bajo `docs/gbitcorp.com/`, presencia local, alt y dimensiones. No se duplicaron assets originales para respetar la protección de los materiales fuente. No migrar `assets/cache`, `backups`, `logs`, `sessions`, `site/config.php` ni credenciales.

## Modelo editorial propuesto

- Modelos: `HomePage`, `ServicePage`/`BusinessPage`, `BlogIndexPage`, `BlogPostPage` y `StandardPage` únicamente para tipos confirmados por la auditoría.
- StreamField: bloques para hero, texto, imagen/copy, tarjetas, grillas de servicios, logotipos, CTA y separadores decorativos. Mantener bloques semánticos y con validación.
- Wagtail Images/Documents: catálogo con alt, caption, focal point y renditions; reusar recursos con manifiesto de procedencia.
- Snippets/settings: navegación, redes, datos de contacto y footer cuando sean realmente globales.
- SEO/URLs: conservar slugs y metadatos observados; redirects explícitos para variaciones `www`/HTTPS y rutas cambiadas.
- PostgreSQL nuevo; nunca importar base ProcessWire sin autorización y un plan de transformación aprobado.

## Limitación por MySQL

La copia local MySQL ya permitió confirmar árbol/rutas públicas, asignaciones template/fieldgroup, campos y estados; ver `15_AUDITORIA_MYSQL_PROCESSWIRE.md` y `16_MODELO_DATOS_PROCESSWIRE.md`. No se revisaron valores sensibles ni contenido de páginas adicionales; las filas de confianza baja/media, taxonomy y asociación completa de assets deben confirmarse antes de definir modelos/migraciones.
