# 17 — Mapeo de contenido ProcessWire a Wagtail

Este mapeo es propuesta de diseño, no implementación. Se fundamenta en asignaciones reales de fieldgroups/templates consultadas en la copia local, plantillas PHP inspeccionadas y contenido/rutas públicas preservadas. No se crearon modelos, bloques ni migraciones.

| ProcessWire observado | Candidato Wagtail | Transformación / revisión |
|---|---|---|
| `home` + sus campos y repeaters | `HomePage` con StreamField de secciones | Hero/copy, líneas de negocio, servicios, partner, equipo, esencia, publicaciones y CTA. Datos de contacto compartidos requieren validar el contenido antes de importar. La sección de esencia tiene copy estructural hardcoded en PHP: no sale del campo y exige curación explícita. |
| `service_service` | `ServicePage` o `BusinessPage` | `subtitle`, `desc`, `image`, `icon`, `content`, `tools`, `clients`; conservar relación y orden de repeaters. Hay 13 filas status On frente a cuatro rutas de servicio públicas documentadas; no publicar las restantes automáticamente. |
| `blog-posts` | `BlogIndexPage` | Lista descendiente de artículos, filtros/paginación solo según comportamiento verificado. |
| `blog-post` | `BlogPostPage` | título, SEO, fecha/publicación, resumen, cuerpo, imágenes y archivos; relaciones a categorías/tags deben migrarse como taxonomy tras revisión. |
| `basic-page`, `eula` | `StandardPage` o clase legal específica | Sanitizar HTML; validar permanencia/vigencia de la ruta. |
| `repeater_*` | bloques StreamField o modelos relacionados/snippets | Mantener tipos de bloque acotados, orden y referencias. No importar páginas repetidoras como páginas de navegación. |
| `field_image`, `field_blog_images`, File/Image fields | Wagtail Images/Documents | Resolver archivos con `pages_id` y nombre en `site/assets/files/<id>/`; verificar archivo, alt, licencia y referencia; generar renditions y metadatos revisados. |
| `field_page` como categorías/tags y relaciones | `ManyToMany` editorial o páginas taxonomy | Mapear por IDs/rutas, no por texto suelto; crear relaciones después de importar nodos destino. |
| `field_metadesc`/SEO y slugs | paneles SEO y `slug` de Wagtail | Preservar URLs del CSV como contrato; validar normalización Unicode, slash final y canonical/redirects. |
| formularios y módulos | formularios Django/Wagtail con integración redefinida | No migrar envíos; confirmar CRM, consentimiento, antispam, permisos y retención. No copiar secretos de Zoho/SMTP ni valores de mensajes. |

## Home: contenido y recursos

El `home.php` confirma que `bannerDesc` alimenta el H1; `carousel_services` obtiene registros de repetidor con imágenes; líneas de negocio enlazan páginas `service`; `carousel_us` alimenta imágenes de Nosotros; `usDesc` alimenta el copy; la esencia está parcialmente hardcoded en PHP; el Home muestra los últimos artículos publicados con miniatura y `resume`; formulario/footer son componentes separados. El campo `social_med` contiene los elementos compartidos. Conteos del Home: 4 elementos de carrusel de servicios, 3 de Nosotros, 3 sociales. No se volcó texto ni datos de contacto. Ver capturas y análisis de imágenes en [14](14_DIAGNOSTICO_HOME_RENDIMIENTO.md) y [reference/home](reference/home/).

Las formas de sección grandes (`Fondo-Blanco-Curvas-03`, fondos curvos y divisores) son candidatas a CSS/SVG responsivo, no a convertir en texto-imagen. Mantener fotografías informativas con focal point y renditions adaptativas; HTML/texto real debe seguir editable. El hero Ciudad-Fondo es 3126×3909 y ~5.05 MB, por lo que debe tener variante/rendition adecuada al viewport y carga prioritaria solo para la imagen visible.

## Seguridad de transformaciones

- Sanitizar HTML permitido del `blog_body`/`desc_html`; no confiar en markup del CMS antiguo ni ejecutar scripts incrustados.
- Omitir campos de password, usuario, sesión, comentarios/contact submissions, datos de contacto privados y configuración de módulo.
- Validar fechas, URLs, alt text, asociaciones entre páginas y referencias a archivos antes de importar.
- La collation source `latin1_swedish_ci` difiere del default de base utf8mb4; definir y probar codificación antes de escritura. La salida de terminal con mojibake no prueba que la fuente esté dañada.

## Hechos / inferencias / pendientes

**Hechos:** fieldgroups y fieldtypes de los templates enumerados existen; el código PHP muestra su uso citado; hay 49 rutas públicas asociadas. **Inferencia:** agrupación exacta final de páginas de negocio en una clase Wagtail común. **Pendiente:** revisar todos los contenidos públicos individualmente, resolver campos HTML y medios, decidir taxonomy y validar formularios con el propietario.
