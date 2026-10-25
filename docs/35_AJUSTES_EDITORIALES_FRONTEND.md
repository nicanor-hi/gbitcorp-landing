# 35 — Ajustes editoriales previos al frontend

**Fase:** 2.2A.3.
**Alcance:** cambios mínimos de esquema/editorial aprobados para preparar el frontend; no se importó contenido.

## Cambios implementados

### Home

- Se agregó `HomePage.hero_image`, FK opcional al modelo configurable de imágenes de Wagtail (`null=True`, `blank=True`, `SET_NULL`, sin imagen predeterminada).
- El campo está expuesto en el panel de edición de Home junto a `hero_copy`.
- La ausencia de imagen es válida y debe seguir siendo segura cuando se construya el template: no hay imagen fallback inventada y el frontend deberá comprobar `hero_image` antes de generar markup/estilos asociados.
- `hero_copy` y los CTA no cambiaron.

### Imágenes dentro de artículos

Se añadió el bloque tipado `ArticleImageBlock` a `BlogPostPage.body`, manteniendo el bloque `rich_text` previo:

- `image`: `ImageChooserBlock` nativo de Wagtail.
- `alt_text`: editable; requerido funcionalmente salvo que la persona editora marque el recurso como decorativo.
- `decorative`: booleano explícito para representar `alt=""` intencional; no se generan descripciones automáticamente.
- `caption`: texto opcional.
- `alignment`: sin alineación, izquierda o derecha. Las dos opciones laterales corresponden a clases de alineación observadas en el HTML público; no se añadió centrado porque la auditoría no lo respalda.
- La validación rechaza imagen ausente, texto alternativo vacío para imágenes no decorativas y alineaciones fuera de las opciones. La estructura se serializa mediante los bloques estándar de Wagtail/StreamField; no admite HTML arbitrario.

No se copiaron ni importaron las 37 imágenes observadas en los cuerpos de artículos.

### Tablas históricas y carruseles

No se agregó `TableBlock` ni bloque genérico de columnas. Según la clasificación documentada en `docs/34_CLASIFICACION_TABLAS_ARTICULOS.md`:

- Ocho tablas de maquetación deberán convertirse en componentes/composición responsive, conservando el contenido y orden de lectura.
- Las dos comparativas del artículo PWA requieren revisión editorial de encabezados antes de modelar su representación semántica.
- Las dos tablas del artículo Cloud requieren resolver el anidamiento con DOM HTML5 antes de transformar.
- Ninguna de las doce tablas está autorizada para conversión automática en esta fase. El futuro proceso debe detener el elemento/página afectada o marcarla para revisión si no puede preservar su contenido; nunca descartarlo silenciosamente.

Los modelos de carrusel de servicios y equipo permanecen sin cambios y diferenciados.

## Migración

Se generó `editorial/migrations/0002_homepage_hero_image_alter_blogpostpage_body.py`.

Revisión previa: contiene únicamente `AddField` para la relación nullable `HomePage.hero_image` y `AlterField` para declarar el nuevo tipo de bloque en `BlogPostPage.body`. El SQL generado para el StreamField fue no-op sobre datos; la operación de esquema añade una columna FK nullable e índice, sin copiar, convertir ni borrar registros.

La configuración se comprobó sin exponer `DATABASE_URL`: destino `gbitcorp_wagtail_dev`, servidor local PostgreSQL en puerto 5432. La migración se aplicó solamente a esa base y terminó correctamente. No se administró el servicio PostgreSQL ni se alteraron otras bases.

## Pruebas y validación

En esta fase se cubren:

- Home sin imagen y con una imagen Wagtail asignada; el campo se conserva tras recargar el modelo.
- Presencia de `hero_image` en la interfaz administrativa Wagtail.
- Bloque de imagen con chooser nativo, campos de accesibilidad/leyenda y opciones laterales justificadas.
- Rechazo de alt vacío en imagen no decorativa y de alineación no permitida; aceptación de imagen decorativa con alt vacío.
- Serialización/deserialización de imagen, caption, alt y alineación en StreamField.
- Compatibilidad de los bloques RichText previos.
- Ausencia de páginas, ancestros, categorías y contenido sembrados automáticamente.
- Integridad de las 49 rutas del manifiesto y sus jerarquías en el árbol temporal de tests.

Resultados al cierre:

- `uv run python manage.py check`: aprobado, sin problemas.
- `uv run python manage.py makemigrations --check --dry-run`: aprobado, sin cambios pendientes.
- `uv run python manage.py migrate --check`: aprobado, sin migraciones pendientes.
- `uv run python manage.py test`: 17 pruebas aprobadas; el test runner creó y eliminó su base temporal.
- `git diff --check`: aprobado; Git mostró únicamente advertencias informativas de normalización LF/CRLF.

## Limitaciones y decisiones pendientes

- El campo opcional permite administrar la imagen de hero, pero no se implementó todavía el template ni la estrategia visual/focal point; el comportamiento de ausencia deberá respetarse en la fase frontend.
- Las imágenes históricas tienen `alt=""` sin resolver si son decorativas o si les falta texto alternativo. La interfaz obliga a tomar esa decisión por recurso, sin inventarla.
- La leyenda se ofrece como campo editorial porque la tarea lo aprueba; la auditoría original no encontró `figure`/`figcaption`, así que no se rellenará automáticamente.
- No se diseñaron ni migraron bloques de tabla. Revisar y actualizar el contrato antes de cualquier cambio futuro que permita representar comparativas o las estructuras ambiguas.
- No se importó contenido ni se aprobó la publicación de ninguna de las 49 rutas. La base permanente conserva solo su estado previo y el esquema actualizado.
- No se instalaron dependencias, Tailwind, Docker ni herramientas HTML adicionales. No se inició el frontend ni FASE 2.2B.
