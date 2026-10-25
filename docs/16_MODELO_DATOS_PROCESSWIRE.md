# 16 — Modelo de datos observado en ProcessWire

## Catálogo de tablas

Conteos exactos obtenidos con `COUNT(*)` en la copia local, por tabla. En `field_*`, los registros suelen ser sparse (una fila solo cuando el campo tiene dato) y algunos contienen IDs o relaciones, no texto. `data` no debe interpretarse sin revisar el fieldtype.

| Tabla | Filas | Tabla | Filas |
|---|---:|---|---:|
| caches | 114 | field_address | 1 |
| field_admin_theme | 0 | field_bannerdesc | 1 |
| field_blog_body | 61 | field_blog_categories | 45 |
| field_blog_comments | 0 | field_blog_comments_max | 0 |
| field_blog_comments_view | 1 | field_blog_comments_votes | 0 |
| field_blog_date | 56 | field_blog_files | 0 |
| field_blog_headline | 0 | field_blog_href | 0 |
| field_blog_images | 76 | field_blog_links | 1 |
| field_blog_note | 0 | field_blog_quantity | 0 |
| field_blog_small | 0 | field_blog_summary | 0 |
| field_blog_tags | 386 | field_carousel_count | 1 |
| field_carousel_services | 1 | field_carousel_us | 1 |
| field_clickable | 0 | field_client | 0 |
| field_clients | 1 | field_columns | 13 |
| field_content | 18 | field_date | 0 |
| field_desc | 160 | field_desc_client | 60 |
| field_desc_html | 9 | field_domain | 3 |
| field_email | 2 | field_email_info | 1 |
| field_features | 8 | field_icon | 186 |
| field_id_id | 4 | field_image | 111 |
| field_img_cover | 8 | field_metadesc | 22 |
| field_pass | 3 | field_permissions | 19 |
| field_phone1 | 1 | field_phone2 | 1 |
| field_process | 25 | field_publish_from | 43 |
| field_publish_until | 0 | field_repeater_scfmessages | 1 |
| field_resume | 54 | field_roles | 5 |
| field_scf_company | 30 | field_scf_date | 30 |
| field_scf_email | 30 | field_scf_fullname | 30 |
| field_scf_ip | 30 | field_scf_message | 30 |
| field_scf_phone | 30 | field_scf_spamip | 0 |
| field_scf_spammail | 0 | field_scf_template | 30 |
| field_service | 0 | field_slider | 1 |
| field_social_med | 1 | field_subtitle | 14 |
| field_title | 718 | field_tools | 4 |
| field_usdesc | 1 | fieldgroups | 56 |
| fieldgroups_fields | 174 | fields | 67 |
| modules | 108 | pages | 762 |
| pages_access | 572 | pages_parents | 174 |
| pages_sortfields | 1 | session_login_throttle | 1 |
| sessions | 717 | templates | 53 |

Total: 80 tablas, de las que 68 son `field_*`. Todos los motores son InnoDB, todas las tablas tienen collation `latin1_swedish_ci`; la base tiene default `utf8mb4_0900_ai_ci`. La auditoría halló cero foreign keys declaradas.

## Tablas estructurales y relaciones

- `pages`: cada página referencia su padre (`parent_id`) y plantilla (`templates_id`), tiene `name`, `status` y metadatos temporales/administrativos. La URL se deriva de la jerarquía y los nombres de página. Índices y claves se inspeccionaron en `INFORMATION_SCHEMA`; el esquema usa IDs enteros y claves/indexes internos de ProcessWire.
- `templates`: nombre y `fieldgroups_id`, además de configuración del template; no se exportaron configuraciones privadas.
- `fields`: definiciones de campos, incluyendo `name`, etiqueta y tipo `Fieldtype*`.
- `fieldgroups` y `fieldgroups_fields`: grupos y orden de los campos asignados a cada template.
- `pages_parents`, `pages_sortfields`, `pages_access`: estructuras de ascendencia, orden y control de acceso. No son sustituto del árbol `pages.parent_id`.
- `modules`: clases y flags registrados; no se inspeccionó la tabla de configuración privada `.data`.
- `caches`, `sessions`, `session_login_throttle`: datos operativos/no editoriales; no migrar ni copiar.

Las columnas habituales dependen del tipo. Campo simple: `pages_id` (normalmente PK) + `data`; Page/Repeater: `pages_id`, `data`, `count`, `parent_id` y orden; multi-value: añade `sort`; Files/Images: `pages_id`, nombre `data`, `sort`, descripción, metadata de archivo y, en imágenes, dimensiones/proporción. Comments tiene columnas personales/operativas. Estas últimas no se documentan con valores ni se incorporarán al importador por defecto. No hay FK declaradas; resolver relaciones con el modelo ProcessWire, no imponiendo integridad basada solo en nombres de columnas.

## Fieldtypes confirmados

Entre los 67 campos registrados aparecen `FieldtypePageTitle`, `FieldtypeText`, `FieldtypeTextarea`, `FieldtypeImage`, `FieldtypeFile`, `FieldtypeRepeater`, `FieldtypePage`, `FieldtypeComments`, `FieldtypeDatetime`, `FieldtypeEmail`, `FieldtypePassword`, `FieldtypeURL`, `FieldtypeCheckbox`, `FieldtypeInteger` y `FieldtypeModule`. Los 68 field tables incluyen además variantes y tablas de módulos. `FieldtypePage` almacena referencias; categorías/tags y permisos/roles son relaciones a páginas, no etiquetas textuales. Repeaters crean páginas hijas con templates `repeater_*`; la columna `data` de las tablas repeater representa IDs/orden según el fieldtype.

## Asignaciones relevantes de campos por template

| Template | Campos relevantes observados |
|---|---|
| `home` | `title`, `metaDesc`, `bannerDesc`, `carousel_services`, `carousel_count`, `carousel_us`, `usDesc`, `address`, `phone1`, `phone2`, `email_info`, `social_med` |
| `service_service` | `title`, `metaDesc`, `subtitle`, `icon`, `image`, `desc`, `columns`, `content`, `tools`, `clients` |
| `blog-post` | `publish_from`, `publish_until`, `blog_date`, `title`, `metaDesc`, `resume`, `blog_body`, `blog_images`, `blog_files`, `blog_categories`, `blog_tags`, comentarios |
| `blog-posts` | `title`, `blog_headline`, `blog_images` |
| `basic-page` | `title`, `image`, `desc_html` |
| `product` | título, SEO, portada/icono, descripción HTML/texto, subtítulo, repetidores `content` y `features`, columnas e imagen |
| `service` | `title`, `id_id`, `desc`, `image` |
| `client` | título, imagen, descripciones |
| `repeater_content` | título, icono, descripción |
| `repeater_tools` | título, icono |
| `repeater_social_med` | título, imagen, URL |

La lista completa de asignaciones fue consultada en metadatos; esta selección prioriza familias públicas observadas. Confirmar todos los campos en el inventario SQL original de la próxima fase antes de transformarlos.

## Estados

Los bits comprobados en core `wire/core/Page.php`: On=1, Locked=4, SystemID=8, System=16, hidden=1024, unpublished=2048, trash=8192. Son flags combinables. SQL contó 762 páginas totales (758 con On, 21 hidden, 46 unpublished, 111 trash, 82 system); por el solapamiento no son buckets aditivos. La publicación debe usar una condición explícita y validada, además de allowlist de páginas/rutas públicas.

## Protección de datos

Se identificaron campos/tablas de contraseñas, sesiones, comentarios, y el repetidor de mensajes de contacto con nombre, correo, teléfono, IP y mensaje. No se leyeron sus valores. Excluirlos del corpus editorial y nunca conservarlos en los informes o la migración. El recuento de esas tablas es metadata; no debe usarse para reproducir registros.
