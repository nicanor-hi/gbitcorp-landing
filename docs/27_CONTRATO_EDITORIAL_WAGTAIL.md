# 27 — Contrato editorial Django + Wagtail

**Estado:** diseño propuesto para revisión; no es autorización de implementación ni importación.
**Alcance de evidencia:** preservación pública, manifiesto vigente, auditorías ProcessWire y revisión de los templates originales pertinentes. No se consultó MySQL en esta fase.

**Trazabilidad:** las decisiones que estaban pendientes en este contrato sobre ancestros de URL, almacenamiento del cuerpo de artículos, cardinalidad de categorías y separación del formulario se resolvieron para diseño en [28_RESOLUCION_DECISIONES_EDITORIALES.md](28_RESOLUCION_DECISIONES_EDITORIALES.md). Ante cualquier diferencia, el documento 28 complementa y prevalece sobre estas propuestas; no constituye autorización de importación.

## 1. Resumen ejecutivo

Este contrato define cómo representar en Wagtail el sitio público preservado. La fuente de alcance es el sitio público y su manifiesto de 49 rutas; la base ProcessWire solo aporta correspondencias de IDs, campos y dependencias. La existencia de páginas, plantillas, registros o archivos históricos no habilita su migración.

Se proponen cinco tipos de página: `HomePage`, `BlogIndexPage`, `BlogPostPage`, `ServicePage` y `EulaPage`. Se propone `StreamField` para composición editorial heterogénea confirmada (Home y servicios), contenido enriquecido para el cuerpo de blog cuando se confirme su estructura, un snippet para las cinco categorías visibles y configuración compartida de sitio para los datos del footer. Las propuestas que no están respaldadas completamente se marcan como pendientes, no como hechos.

El CSV del manifiesto contiene **49 rutas únicas y 49 IDs únicos**, distribuidas en 1 Home, 1 índice, 42 artículos, 4 servicios y 1 EULA. Las 49 están clasificadas como vigentes públicamente, pero `import_authorized` permanece en “No” para todas. Por tanto, “pública confirmada” no equivale a “aprobada para importar” o “publicar”.

## 2. Evidencia, alcance y vocabulario

Las afirmaciones de este documento se distinguen así:

- **Confirmado:** respaldado por preservación, manifiesto, auditoría o código original identificado.
- **Propuesta:** contrato recomendado para la futura aplicación; requiere revisión antes de implementarse.
- **Pendiente:** la evidencia disponible no basta para fijar comportamiento, contenido o relación.

Fuentes del proyecto: [manifiesto vigente](21_MANIFIESTO_CONTENIDO_VIGENTE.md) y [CSV del manifiesto](21_MANIFIESTO_CONTENIDO_VIGENTE.csv), [clasificación editorial](22_CLASIFICACION_EDITORIAL.md), [inventario de assets vigentes](23_INVENTARIO_ASSETS_VIGENTES.md), [preparación del importador](24_PREPARACION_IMPORTADOR_WAGTAIL.md), [cierre de auditoría](25_CIERRE_AUDITORIA_PROCESSWIRE.md), [modelo de datos ProcessWire](16_MODELO_DATOS_PROCESSWIRE.md) y [mapeo previo](17_MAPEO_CONTENIDO_WAGTAIL.md).

La jerarquía de decisión es:

1. Capturas, rutas, contenido visible e interacciones preservadas determinan el alcance público.
2. El manifiesto identifica correspondencias públicas verificadas y dependencias.
3. ProcessWire aporta el origen de algunos valores y relaciones, pero no amplía el alcance.

Se excluyen por defecto páginas no manifestadas, las 762 páginas históricas, las nueve páginas `service_service` adicionales, las 191 referencias/destinos de tags sin uso público confirmado, contenido administrativo y registros sensibles. Tampoco se incorporan los 728 archivos en bloque. Las clasificaciones A/B/C/D conservan el significado establecido en el documento 22; C y D no forman parte de la migración pública.

## 3. Inventario de tipos de página y cobertura

| Tipo propuesto | Plantilla ProcessWire | Cantidad pública | Rutas preservadas | Estado de correspondencia |
|---|---|---:|---|---|
| `HomePage` | `home` | 1 | `/` | Confirmada en manifiesto |
| `BlogIndexPage` | `blog-posts` | 1 | `/blog/posts/` | Confirmada en manifiesto |
| `BlogPostPage` | `blog-post` | 42 | `/blog/posts/<slug>/` | Confirmadas en manifiesto |
| `ServicePage` | `service_service` | 4 | Cuatro rutas `/negocio/.../.../` | Confirmadas en manifiesto; ancestros estructurales por validar |
| `EulaPage` | `eula` | 1 | `/eula/quickbook/` | Confirmada en manifiesto; ancestro estructural por validar |
| **Total** |  | **49** | 49 rutas únicas | No existe aprobación de importación |

Las rutas concretas, slugs e IDs se mantienen en el CSV fuente, evitando duplicar y desincronizar el inventario aquí. La comprobación del manifiesto confirma una fila por ruta, unicidad de ruta e ID, y distribución 1/1/42/4/1 por template.

## 4. Jerarquía editorial y URLs

### 4.1 Árbol propuesto

```text
Wagtail root / Site.root_page
└── HomePage (única; URL pública /)
    ├── contenedores estructurales de blog (si son necesarios para la ruta exacta)
    │   └── BlogIndexPage (URL pública /blog/posts/)
    │       └── BlogPostPage (42 rutas públicas /blog/posts/<slug>/)
    ├── contenedores estructurales de negocio (si son necesarios)
    │   └── ServicePage (4 rutas públicas /negocio/.../.../)
    └── contenedor estructural legal (si es necesario)
        └── EulaPage (URL pública /eula/quickbook/)
```

Este dibujo expresa únicamente una forma de alcanzar rutas y tipos válidos, no confirma que cada segmento intermedio sea una página pública o una página editable. La preservación confirma los paths, pero el manifiesto disponible no prueba por sí solo los IDs/parents de cada ancestro intermedio. Antes de implementar, verificar los padres reales contra las relaciones auditadas y decidir si hacen falta páginas estructurales no públicas o una jerarquía alternativa que conserve las URLs. No inventar páginas de navegación públicas para llenar segmentos.

### 4.2 Restricciones Wagtail propuestas

- `HomePage`: una instancia (`max_count = 1`), bajo la raíz del árbol, configurada como `Site.root_page`; sin páginas Home descendientes.
- `BlogIndexPage`: una instancia en el alcance inicial; permitir únicamente `BlogPostPage` como hijos editoriales.
- `BlogPostPage`: solo bajo `BlogIndexPage`; hoja salvo evidencia futura que justifique hijos.
- `ServicePage`: solo bajo el contenedor estructural de negocio que se confirme. No limitar el modelo global a cuatro para siempre; el manifiesto/importación inicial autorizaría como máximo las cuatro correspondencias examinadas.
- `EulaPage`: una instancia en el alcance inicial; bajo la estructura necesaria para preservar `/eula/quickbook/`.
- Los contenedores estructurales deben ser explícitos y no deben adquirir contenido, navegación ni publicación pública sin evidencia y aprobación.

Wagtail ofrece restricciones nativas `parent_page_types`, `subpage_types`, `max_count` y validaciones de árbol que conviene usar para expresar este contrato. Deben probarse además los paths finales; validar el padre no sustituye validar URL.

### 4.3 Conservación de rutas

Usar slugs de la URL pública preservada como referencia editorial principal. Mantener la jerarquía necesaria para que Wagtail resuelva exactamente las 49 rutas. No normalizar, traducir ni cambiar slugs durante importación sin decisión explícita. Los ancestros solo se crean si son necesarios para la ruta y se clasifican como estructura, no como contenido A adicional. No se diseñan ni implementan redirecciones en esta fase.

## 5. Matriz propuesta de modelos y campos

Los nombres de campos son conceptuales. La implementación debe usar campos nativos de Wagtail cuando existan (por ejemplo `Page.title`, `Page.slug`, `Page.search_description`) y evitar duplicarlos con nombres propios. `null`/vacío, cardinalidad, validación HTML y editor de cada campo se deben especificar en el código y tests de FASE 1.2B.

| Modelo | Campos propuestos | Correspondencia y reglas | Representación futura |
|---|---|---|---|
| `HomePage` | Nativos `title`, `slug`, `search_description`; `hero_heading`/copy (origen `bannerDesc`); `sections` (`StreamField`); referencias a imágenes según bloque; sin duplicar contacto/social en la página si se centraliza en settings | Una página; `bannerDesc` es el origen confirmado del texto del banner. Los 10 registros repetidores observados son 4 filas `carousel_services`, 3 `carousel_us`, 3 `social_med`; respetar orden. `carousel_count` es derivable/auxiliar y no se migra como verdad independiente. Copy “Nuestra esencia” está hardcodeado en PHP, necesita curación editorial antes de introducirse como editable | Template de Home con secciones ordenadas; navegación/footer compartidos |
| `BlogIndexPage` | Nativos `title`, `slug`, `search_description`; `header_image` opcional; orden/categorías asociados según evidencia | Origen de imagen de cabecera: primera `blog_images` del índice (ID 1037). `blog_headline` aparece comentado en template: no usar como sección visible. Filtros muestran cinco categorías confirmadas; asignación requiere aprobación editorial | Índice de artículos, filtros y tarjetas; no dar por vigente paginación: su código observado está comentado |
| `BlogPostPage` | Nativos `title`, `slug`, `search_description`; `summary` (ProcessWire `resume`); `body` (`RichTextField` o estructura revisada); `lead_image`; categorías M2M a snippet; fecha de orden/publicación solo tras confirmar semántica | Las 42 páginas están en el manifiesto. El template usa `blog_body` como contenido, `resume` en tarjetas y primera imagen de `blog_images` como banner/tarjeta. `publish_from` interviene en orden del listado de Home; `blog_date` y `publish_until` existen en esquema pero no deben migrarse sin prueba de su uso editorial público. Tags/comentarios/archivos no se incluyen por defecto | Detalle de artículo; tarjetas en índice/Home; relación a categorías |
| `ServicePage` | Nativos `title`, `slug`, `search_description`; `banner_image` desde `image`; `description` enriquecida desde `desc`; `content_blocks` ordenados; `tools` ordenadas | Cuatro páginas públicas; 19 elementos de contenido y 64 elementos de herramientas observados. El campo `columns` controla presentación fija, no contenido; no migrar. `subtitle`, `icon` de página y `clients` no aparecen confirmados como salida pública del template y quedan fuera salvo nueva evidencia | Detalle de servicio con imagen de banner, grupos de contenido y herramientas |
| `EulaPage` | Nativos `title`, `slug`, `search_description` si el SEO público lo confirma; `legal_body` con formato capaz de preservar estructura literalmente | Única ruta `/eula/quickbook/`. Texto legal observado reside en el template PHP, no se confirmó campo de base de datos; preservar literalmente desde evidencia pública con aprobación legal/editorial. No inventar versión ni fecha | Documento legal de lectura; no reescritura |

### Publicación y revisión editorial

El que una ruta sea pública no autoriza su publicación en el nuevo CMS. Importación inicial propuesta a borrador/no publicada, con revisión del responsable editorial. La publicación será una acción explícita. Mantener cualquier estado histórico como dato informativo de importación, no como orden automática de publicar, salvo aprobación específica.

## 6. Diseño propuesto de StreamField y bloques

StreamField es apropiado cuando la página requiere una secuencia heterogénea de secciones editables. No debe sustituir automáticamente un cuerpo que realmente sea un único documento de texto enriquecido. Sus bloques y validaciones deben reflejar estructuras observadas, no una abstracción universal.

| Bloque propuesto | Campos conceptuales | Uso/evidencia | Restricciones y pendiente |
|---|---|---|---|
| `HeroSectionBlock` | encabezado/copy; imagen o fondo solo si recurso confirmado; CTA con texto y destino | Home: banner visible; `bannerDesc` confirma copy de banner | Definir si imagen y CTA son administrables y accesibles tras contrastar capturas; no convertir copy en imagen |
| `ServiceLinksSectionBlock` | título opcional, lista ordenada de referencias/etiquetas de servicios | Home: cuatro líneas de negocio enlazan a cuatro servicios | Rótulos y códigos se resuelven en PHP; confirmar el texto público y el destino por cada elemento antes de importarlo |
| `ServiceCarouselSectionBlock` | lista ordenada de imágenes; título/alt y enlace solo cuando estén evidenciados | Home: cuatro filas repetidoras `carousel_services`, imágenes en carrusel | Validar cardinalidad real por fila, orden, texto alternativo y comportamiento; no crear campos no observados |
| `PartnerSectionBlock` | logotipos/imágenes, copy y enlace externo como campos independientes | Home: sección de partner Zoho observada con dos imágenes/CTA | Destino externo se conserva como referencia y no se navega; revisar vigencia/licencia y copy antes de carga |
| `AboutSectionBlock` | copy (`usDesc`) y secuencia ordenada de imágenes | Home: tres filas `carousel_us` y texto descriptivo | Texto alternativo actual genérico necesita revisión; determinar si carrusel requiere una lista bloqueada o bloques repetibles |
| `TextSectionBlock` | encabezado y texto enriquecido | Home: contenido de “Nuestra esencia” está en código, no DB | Requiere transcripción/revisión de captura y decisión editorial; no presumir fuente DB |
| `FeaturedPostsSectionBlock` | selección ordenada de referencias a artículos o regla de selección explícita | Home presenta los dos más recientes por `publish_from` | Preferir selección automática “dos más recientes” solo si se aprueba la regla; actualmente plantilla lo hace. No crear relación editorial nueva sin validar fechas y desempate |
| `ContactSectionBlock` | solo estructura y textos públicos aprobados; integración no embebida en modelo | Home muestra zona de contacto y formulario Zoho | Campos, destinatario, consentimiento, privacidad y envío requieren autorización. Esta fase no diseña envío ni registra submissions |
| `ServiceOfferingBlock` | `title`, `icon`/imagen, `description` enriquecida | Servicios: los 19 elementos de `content` presentan icono, título y descripción | Orden preservado; validar cardinalidad por página, HTML y si icono es imagen o fuente/vector |
| `ServiceToolsBlock` o lista de herramientas | logo/imagen ordenada; etiqueta accesible solo si validada | Servicios: 64 herramientas; template muestra icono | No hacer etiquetas visibles que el original no mostraba; texto accesible alternativo sí requiere revisión. Comparar si conviene un único bloque con elementos repetibles |
| `LegalTextBlock` (opcional) | texto enriquecido/estructura legal | EULA si el texto debe segmentarse para edición | Preferible un único campo de texto legal con formato si conserva literalmente el documento. Solo usar bloque si el contenido preservado demuestra secciones distinguibles |

**Decisión propuesta:** Home usa un `StreamField` con tipos limitados a secciones confirmadas, permitiendo orden editorial. Servicios usan StreamField para los 19 ítems de contenido, más una colección ordenada de herramientas (un StreamField solo si la secuencia necesita alternar tipos distintos). El cuerpo de blog empieza como RichTextField si la revisión de las 42 páginas demuestra un documento predominantemente textual; si existen estructuras heterogéneas repetidas, diseñar bloques concretos a partir de ejemplos reales antes de implementar.

### 6.1 Elementos de Home confirmados y límites

El template original muestra, en orden general, hero, enlaces de líneas de negocio, carrusel de servicios, sección de partner, sección “Nosotros” con copy/imágenes, “Nuestra esencia”, dos artículos destacados y contacto/formulario; el footer es compartido. El orden visual exacto y variantes responsive se validan con [capturas preservadas](reference/). Este orden no convierte cada elemento en bloque importable: contenido hardcodeado, vínculos externos, copy de formulario y assets requieren validación/selección.

Los 10 repetidores se interpretan como registros auxiliares que alimentan tres componentes compartidos/repetidos, no como diez páginas ni diez secciones. El `carousel_count` se calcula del contenido para evitar un contador duplicado incoherente.

## 7. Blog, taxonomía y relaciones

### 7.1 Categorías

La web preservada presenta cinco categorías y la auditoría confirma relaciones de uso. Propuesta: snippet `BlogCategory` no navegable, con `name`, `slug` estable y `sort_order` explícito para el orden del filtro. Relación M2M desde `BlogPostPage`; comprobar si una publicación puede tener más de una categoría y si el filtro necesita una sola elección. Solo las cinco etiquetas/categorías cuya presencia se confirma públicamente entran como candidatas; no crearlas/importarlas sin aprobación.

No usar categorías como páginas Wagtail salvo que se apruebe una URL pública propia para cada categoría. Las 191 referencias de tags no están respaldadas por uso visible y quedan fuera.

### 7.2 Artículos y fechas

Una publicación es hija del índice, mantiene su slug. `publish_from` se utiliza en el template de Home para ordenar los dos artículos destacados, pero debe confirmarse si representa fecha editorial/publicación y cómo manejar nulos/desempates. `blog_date` no está confirmado como visible; `publish_until` no implica expiración en el nuevo sitio. No migrar fechas o programación histórica a publicación automática sin decisión.

El cuerpo `blog_body` se renderiza como HTML en la plantilla. La implementación debe desinfectar/normalizar de forma segura y preservar estructura pública. La auditoría observó una referencia de código `blog_resume` para artículos relacionados frente al campo de esquema `resume`; tratarlo como discrepancia pendiente, no suponer que hay un campo nuevo.

La página 1086 ilustra que `title` de ProcessWire puede no ser el encabezado del cuerpo: el título DB tiene doble espacio; el template deja comentada la salida de `$page->title` dentro de un H4 y el H2 visible pertenece al cuerpo. Para Wagtail, el contenido visible preservado es referencia editorial; SEO title y encabezado de cuerpo son conceptos separados. No hacer reemplazos automáticos de espacios como corrección editorial general.

## 8. Snippets, datos compartidos y configuración del sitio

- **`BlogCategory` snippet (propuesta):** taxonomía para las cinco categorías visibles; no se convierte en página ni se autoimporta.
- **Configuración de sitio (propuesta):** una entidad de settings Wagtail por sitio para valores compartidos de footer/contacto/social, separada del Home. La auditoría observó tres filas `social_med`, más `address`, `phone1`, `phone2`, `email_info`; los valores no se replican aquí ni se consideran automáticamente aprobados. Validar cuáles se muestran hoy y con qué privacidad antes de incorporarlos.
- **`SocialLink` ordenado:** si se requiere panel editorial independiente y orden, relacionarlo como child/orderable de settings, no como snippet genérico. Conservar tipo, URL y orden solo con evidencia pública. No incluir credenciales o identificadores privados.
- **Nada de snippets para cada elemento visual:** los items del carrusel, ofertas de servicio y herramientas pertenecen a la secuencia de su página y su orden; mantenerlos como bloques/relaciones inline salvo que otra página comparta la misma entidad con prueba.

En Wagtail los snippets son modelos Django fuera del árbol de páginas y no tienen URL por defecto; además no son ordenables automáticamente en el admin. Por eso son adecuados para la taxonomía sin URL, pero no necesariamente para listas cortas cuyo orden define el diseño.

## 9. Imágenes y documentos

Usar biblioteca Wagtail para imágenes editoriales confirmadas: imagen principal de artículo, imagen de cabecera de índice, imágenes de Home/carruseles, banner e iconografía de servicios cuando sean recursos con significado. Los campos de imagen deben incorporar texto alternativo revisado, focal point y renditions responsivas. Para documentos, usar `Document`/bloque de documento únicamente cuando exista una descarga pública preservada; `blog_files` no tiene uso confirmado en las 42 páginas.

La auditoría documenta 933 apariciones de recursos agrupadas en 239 URLs/tipos, 226 recursos locales y 13 sin coincidencia local; “sin coincidencia” no significa automáticamente roto. Hay 728 archivos ProcessWire disponibles, pero no se importan en bloque. Referencias consultadas confirmaron 172 referencias de media A/B (75 `blog_images`, 83 icon, 14 image) en archivos existentes; la selección editorial final queda sujeta al inventario de assets vigente y revisión por página.

Las imágenes funcionales deben tener alt útil; las decorativas, alt vacío. No asumir que los `alt` actuales son adecuados (el carrusel “Colaboradores” es señal para revisión). No depender de rutas absolutas Windows. Mantener IDs/rutas históricas en mapa de importación, no en URLs de media públicas.

Fondos/separadores estructurales deben resolverse preferentemente con CSS/SVG responsive o recursos adaptativos. Conservar ilustraciones que aporten valor; no guardar textos en imágenes. Usar renditions/Wagtail para servir tamaños adecuados, `srcset` y focal point, evitando descargar masters grandes en móvil. Validar seguridad del formato SVG antes de permitir carga editorial.

## 10. Correspondencia ProcessWire → Wagtail

| Origen ProcessWire | Evidencia de uso público | Destino propuesto | Estado |
|---|---|---|---|
| `pages` + `templates` | 49 coincidencias exactas de ruta/ID/template en manifiesto | Una de las cinco clases por ruta permitida | Correspondencia confirmada; importación no aprobada |
| `title`, `metaDesc` | Títulos/meta observados en template compartido, según tipo | `Page.title`, `Page.search_description`; campos separados solo si SEO title difiere | Confirmar casos específicos y normalización |
| Home `bannerDesc`, repetidores | Hero, carruseles, partner, about y social visibles | Campos Home/StreamField/settings | Estructura confirmada; valores sujetos a revisión editorial |
| `resume`, `blog_body`, `blog_images` | Tarjetas, detalle y primera imagen usada | summary, cuerpo enriquecido, lead image | Uso confirmado; 1086 y HTML requieren revisión |
| `blog_categories` | Filtros/relaciones visibles | `BlogCategory` + relación ordenada o M2M | Cinco categorías públicas confirmadas, importación pendiente |
| `content`, `tools` en servicios | 19 ofertas y 64 iconos/herramientas | Bloques/colecciones ordenadas | Uso y conteo confirmados; etiquetas de herramientas no confirmadas |
| `columns`, `clients` en servicio | No confirmados como contenido renderizado en template actual | Omitir en modelo público inicial | Excluidos por falta de uso público demostrado |
| `blog_tags`, comentarios, `blog_files` | No observados como contenido vigente en las páginas preservadas | Excluir del contrato inicial | No migrar por defecto |
| EULA hardcoded en `eula.php` | Documento legal público preservado | Campo legal literal en `EulaPage` | Contenido debe validarse/aprobarse; no hay mapeo DB confirmado |
| assets `site/assets/files/` | Inventario visual público + referencias de campos | Wagtail Images/Documents seleccionados | Solo recursos confirmados, no copia masiva |

## 11. Validaciones del modelo y edición

Reglas recomendadas para tests de FASE 1.2B:

1. Solo puede existir una `HomePage`, una `BlogIndexPage` y una `EulaPage` en el alcance inicial.
2. Cada `BlogPostPage` es hija del índice; servicios y EULA respetan padres estructurales aprobados.
3. Las URLs resueltas de las 49 filas del manifiesto son exactamente iguales a las rutas públicas, sin colisiones ni barras faltantes.
4. No se crean páginas fuera de la allowlist del manifiesto durante importación.
5. Los streams preservan orden; un bloque exige solo campos pertinentes y valida enlaces/imagen alternativos.
6. Categorías tienen slug único y orden explícito; no se admiten categorías históricas por asociación accidental.
7. Cuerpo HTML permite solo formato seguro; se preservan entidades/texto en Unicode y se comprueban ejemplos antes de importación.
8. Las referencias a assets fallidas se reportan, no se reemplazan silenciosamente por archivo histórico homónimo.
9. Estado importado inicia como borrador/no publicado y requiere aprobación editorial explícita.
10. Las reglas de featured posts, fechas y disponibilidad tienen comportamiento determinista y tests de valores vacíos/desempates.
11. Formulario no envía nada durante importación ni pruebas; destino, consentimiento y tratamiento de datos quedan sujetos a contrato separado.

## 12. Contrato de importación futura

La unidad de entrada debe ser el manifiesto aprobado, no un escaneo general de `pages` ni de assets.

- Mantener el CSV vigente como allowlist de rutas/IDs y añadir aprobación editorial en un campo revisado por responsable, sin inferirla de la clase A.
- Mantener un registro auxiliar privado/interno `LegacyPageMap` y `LegacyAssetMap` (nombres propuestos) con `source_system`, ID ProcessWire único, ruta histórica, checksum/ruta relativa de archivo cuando proceda y FK al destino Wagtail. Evitar exponer IDs de origen en campos editoriales públicos.
- Identidad idempotente: clave única por sistema + ID histórico (y por asset su ID/ruta normalizada); una segunda ejecución actualiza el mismo mapeo, no duplica página/media.
- Antes de importar: dry-run, validar 49 rutas exactas, padres, unicidad, campos obligatorios, codificación, recursos y aprobación; producir resumen redactado.
- Importar únicamente destinos autorizados, inicialmente como borrador, sin publicar ni activar envío de formularios.
- Conservar slugs y registrar diferencias de URL para revisión; redirecciones se definirán en etapa posterior.
- Fallar de manera visible ante una referencia desconocida; no ampliar allowlist automáticamente ni completar con registros C.
- El mapeo y logs no deben contener secretos ni valores privados de formularios/usuarios.

La posibilidad de poner los mapas como modelos internos de Django o en una tabla de correspondencias separada se decidirá en implementación. No hay necesidad demostrada de añadir los IDs antiguos a todas las páginas públicas.

## 13. Riesgos y decisiones pendientes

| Tema | Evidencia/impacto | Estado/decisión necesaria |
|---|---|---|
| Padres estructurales de blog, servicios y EULA | Paths preservados, pero padres/ancestros exactos no quedan resueltos por el CSV | **Pendiente bloqueante para cerrar `parent_page_types` y URL tests**; verificar manifiesto enriquecido/relaciones antes de implementar |
| Autorización de importación | 49 rutas públicas, todas con `import_authorized=No` | **Pendiente editorial**; ninguna página debe publicarse/importarse automáticamente |
| HTML/codificación | CP1252/latin1, cuerpos y resúmenes tienen casos dudosos previos; la literalidad es importante | **Pendiente** para revisión de muestras con capturas; no corregir signos o entidades heurísticamente |
| Categorías | Cinco visibles, orden/labels y asignación exacta requieren aprobación | **Pendiente editorial** |
| Home hardcoded | “Nuestra esencia”, partner, enlaces de negocio y formulario incluyen contenido/decisiones en PHP | **Pendiente** de transcripción y aprobación; no migrar código como fuente de texto sin revisión |
| Contacto Zoho | Integración externa visible; efecto de envío, privacidad y destino | **Pendiente bloqueante para implementar envío**; no probar envíos |
| Servicios | `subtitle`/`icon` y `clients` no confirmados en salida; tools muestran iconos sin nombre visible | Excluir campos no confirmados; revisar alt y si el texto accesible requiere etiqueta aprobada |
| Artículos | `blog_resume` en consulta de relacionados vs `resume`; fechas inconsistentes/semántica | Resolver antes de reglas de relacionados/featured y publicación programada |
| EULA | Contenido legal está hardcoded, no DB; riesgo de alterar términos | Aprobación legal del texto exacto antes de publicación |
| 13 recursos sin match local | Pueden ser URLs externas/dinámicas/renombradas, no necesariamente rotas | Revisar por contexto y URL; excluir del paquete hasta determinar uso |
| Separadores responsive | Imágenes estructurales pueden escalar/cortarse | Reimplementar intención con CSS/SVG/adaptativos; comprobar capturas multi-viewport en fase frontend |

### Decisiones propuestas para aprobar antes de FASE 1.2B

1. Mantener los cinco modelos propuestos y la jerarquía limitada descrita.
2. Usar StreamField para Home y la secuencia de ofertas de servicio; RichText para artículo solo si la revisión de cuerpos lo respalda.
3. Representar categorías visibles como snippet no navegable; no incorporar tags.
4. Separar settings compartidos de footer/social de Home, tras aprobar los datos públicos.
5. No migrar contenido, publicar páginas ni activar formulario hasta autorización explícita.

## 14. Plan de implementación de FASE 1.2B

1. Resolver ancestros/IDs de ruta; confirmar contratos de padre e hijos con el manifiesto.
2. Obtener aprobación editorial de importación y revisión de campos ambiguos (resúmenes, cuerpos, categorías, EULA, datos de contacto, alt y los 13 recursos sin match).
3. Definir la app editorial, modelos `Page`, restricciones de árbol, settings/snippets y nombres finales de campos.
4. Implementar bloques acotados a estructuras observadas; decidir RichText/StreamField para blog con muestras representativas.
5. Crear migraciones de esquema vacías de contenido; no importar ProcessWire en esta fase salvo autorización específica posterior.
6. Añadir tests de jerarquía, singleton, URL, orden de bloques, categorías, permisos editoriales y borradores.
7. Revisar el admin de Wagtail y comprobar edición sin construir aún el frontend completo.
8. Documentar decisiones definitivas y detenerse para aprobación antes de una fase de frontend/importación.

## 15. Criterios de aceptación de este contrato

- Los cinco tipos originales están representados por propuestas explícitas.
- Las 49 rutas del manifiesto se cubren en distribución 1/1/42/4/1; no se agregan rutas históricas.
- Se separan contenido A, dependencias B, histórico C e interno/sensible D.
- Jerarquías, campos, StreamField, taxonomía, media y URLs tienen reglas verificables o pendientes explícitos.
- El mapeo no convierte la presencia en DB en autorización editorial.
- La importación futura tiene allowlist, dry-run, idempotencia y publicación controlada.
- No se implementa modelo, migración, consulta DB, importación ni frontend en FASE 1.2A.
- La revisión editorial y las decisiones bloqueantes quedan visibles antes de la FASE 1.2B.

## Referencias técnicas oficiales

- [Modelos de páginas y restricciones de árbol en Wagtail 7.4](https://docs.wagtail.org/en/stable-7.4.x/reference/models.html)
- [StreamField en Wagtail 7.4](https://docs.wagtail.org/en/v7.4/topics/streamfield.html)
- [Snippets en Wagtail 7.4](https://docs.wagtail.org/en/stable-7.4.x/topics/snippets/)
- [Imágenes, renditions y focal points en Wagtail 7.4](https://docs.wagtail.org/en/stable-7.4.x/topics/images.html)
- [Bloques de StreamField](https://docs.wagtail.org/en/stable-7.4.x/reference/streamfield/blocks.html)
