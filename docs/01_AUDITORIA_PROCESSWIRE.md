# 01 — Auditoría del respaldo ProcessWire

## Alcance y método

Inspección estática de `docs/gbitcorp.com/`, sin iniciar PHP, ProcessWire ni sus módulos, y sin editar archivos. No se consultó la base MySQL. El respaldo completo queda fuera de Git por `.gitignore`.

## Hechos comprobados

- Versión declarada por el core: **ProcessWire 3.0.229**, en `wire/core/ProcessWire.php` (`versionMajor=3`, `versionMinor=0`, `versionRevision=229`). `index.php` declara índice mínimo 300.
- Raíz: `wire/` (CMS/core), `site/` (personalizaciones/activos) y archivos de arranque y metadatos. `site/` contiene `templates/`, `modules/` y `assets/`.
- Conteo total inspeccionado: 3,786 archivos.
- `site/templates/`: 206 archivos en total, incluidos 44 PHP, 24 CSS, 29 JS, 83 imágenes raster, 3 SVG, 11 fuentes (`ttf`, `woff`, `woff2`, `eot`) y recursos adicionales.
- Plantillas PHP representan portada, servicios, negocio, clientes, blog/posts/categorías/tags, casos de éxito, páginas básicas, EULA, contacto, equipo y salidas de formulario. Hay variantes `old`/`copy`/`bk` que requieren confirmar uso antes de migrar.
- `site/assets/files/`: 728 archivos (407 PNG, 259 JPG, 58 GIF, 3 JPEG y 1 TXT). Son archivos de contenido administrado; la asociación archivo-página requiere MySQL.
- La estructura también contiene `assets/cache`, `backups`, `logs` y `sessions`; no migrar su contenido operativo, cachés, sesiones o backups.
- Directorios de módulos locales: `.SimpleContactForm`, `Helloworld`, `InputfieldCKEditor`, `MarkupBlog`, `MarkupSocialShareButtons`, `NewsletterSubscription`, `SchedulePages`, `SimpleContactForm` y `WireMailSmtp` (la carpeta `.SimpleContactForm`/`SimpleContactForm` aparece como dos directorios distintos en Windows). La carpeta incluye componentes del core y terceros; no se puede deducir estado activo desde archivos solamente.
- Se observan estilos/scripts actuales bajo `templates/css/new`, `templates/js/new`, `templates/scripts` y carpetas antiguas `css/old`, `js/old`, además de `styles/` y `css/default`.

## Formularios e integraciones

- La portada pública contiene un formulario POST hacia Zoho CRM WebToLead. El envío no se probó. Confirmar organización/cuenta, destino vigente, consentimiento, captcha, campos y tratamiento de datos.
- Hay módulos SimpleContactForm, NewsletterSubscription y WireMailSmtp. Su presencia no demuestra que estén activos o usados por páginas actuales.
- Hay referencia a Google Maps API en un template antiguo; se detectó configuración tipo clave en el respaldo, no reproducida aquí. Revisar necesidad y rotar si aún tuviera vigencia.
- No se inspeccionaron los valores de `site/config.php`; ese archivo y credenciales de integración no deben migrarse.

## Dependencias de MySQL y límites

ProcessWire almacena páginas, árboles, slugs, asignación de plantillas/campos, opciones, categorías, contenido de blog y vínculos entre registros en MySQL. Los archivos bajo `assets/files` no contienen por sí solos el contexto suficiente para reconstruir todas sus asociaciones. Sin la base no se recuperan páginas privadas/no enlazadas, campos personalizados, historial, usuarios, formularios enviados, preferencias de módulos o jerarquías completas.

## Inferencias y pendientes

- Las carpetas antiguas parecen conservar implementaciones previas, pero su uso debe verificarse con referencias desde plantillas activas y páginas públicas.
- La presencia de módulos es evidencia de disponibilidad en el respaldo, no de que estén habilitados en producción.
- Pendiente: inventario de referencias por plantilla y correspondencia de imágenes de `assets/files` con cada página usando export MySQL autorizado o revisión manual en admin.
- Pendiente: determinar vigencia de EULA, vacantes, newsletter, mapas y todos los destinos de integraciones.

## Protección y verificación

El respaldo se inspeccionó como lectura únicamente. La versión y estructura se consultaron desde el filesystem; no se ejecutó el código original. En esta fase no se realizaron escrituras dentro de `docs/gbitcorp.com/`.
