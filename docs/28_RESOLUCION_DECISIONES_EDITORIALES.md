# 28 — Resolución de decisiones editoriales Wagtail

**Estado:** decisiones de diseño para revisión; no autoriza implementación, importación ni publicación.
**Alcance:** análisis de las 49 rutas preservadas, informes de auditoría, CSV de manifiesto, templates ProcessWire pertinentes y documentación oficial de Wagtail 7.4. No se accedió a MySQL. No se modificaron ProcessWire ni `docs/reference/`.

Este documento resuelve las propuestas pendientes de [27_CONTRATO_EDITORIAL_WAGTAIL.md](27_CONTRATO_EDITORIAL_WAGTAIL.md). No cambia el alcance editorial: las 49 rutas del manifiesto son las únicas páginas públicas vigentes confirmadas; todas siguen con `import_authorized=No`.

## 1. Resumen de decisiones

| Tema | Decisión técnica | Estado restante |
|---|---|---|
| Jerarquía URL | Usar el árbol nativo de Wagtail y siete páginas estructurales `RouteContainerPage` para los segmentos intermedios que no son rutas A del manifiesto | Resuelta técnicamente; hay que probar padres, slugs, URL y 404 en implementación |
| Artículos | Campo editorial final `StreamField` de bloques tipados, con `RichTextBlock` limitado para fragmentos de texto; HTML ProcessWire se conserva solo en staging inerte hasta conversión y revisión | Elección de almacenamiento resuelta; catálogo completo de bloques requiere inventario de estructuras y no bloquea crear modelos vacíos |
| Categorías | Snippet `BlogCategory`, relación múltiple muchos-a-muchos con `BlogPostPage`, slug único y orden explícito | Resuelta técnicamente; etiquetas y asignaciones requieren aprobación editorial |
| EULA | Un campo `RichTextField` con features allowlist y estructura semántica restringida; no reescribir ni normalizar el texto legal | Resuelta técnicamente; contenido exacto y publicación requieren aprobación legal/editorial |
| Zoho | El modelo editorial solo configura presentación; envío queda en integración funcional separada y aún no especificada | Resuelta separación; integración bloqueada por falta de contrato/decisión |

## 2. Cobertura y regla de alcance

El manifiesto fue comprobado con **49 rutas únicas y 49 IDs únicos**: 1 `home`, 1 `blog-posts`, 42 `blog-post`, 4 `service_service` y 1 `eula`. Las rutas vigentes coinciden con la distribución de [21_MANIFIESTO_CONTENIDO_VIGENTE.csv](21_MANIFIESTO_CONTENIDO_VIGENTE.csv). Las páginas históricas, las nueve adicionales `service_service`, los destinos de tags sin uso público y los archivos no confirmados siguen excluidos por defecto.

La existencia de una ruta en la preservación confirma vigencia pública, no autorización para importar/publicar. Ninguna ruta se autoriza en este documento. Dependencias técnicas solo pueden servir para construir las 49 rutas; no se convierten en nuevas páginas A.

## 3. Jerarquía exacta para las rutas preservadas

Wagtail genera `url_path` a partir del slug y del padre. Para reproducir los paths con la jerarquía nativa, los segmentos intermedios deben existir en el árbol. El CSV identifica 49 destinos, pero no incluye en cada fila los IDs ProcessWire de esos ancestros. Por ello el diseño fija los slugs/rutas estructurales derivados de los destinos públicos, sin atribuirles IDs ni contenido ProcessWire.

### 3.1 Matriz de nodos estructurales

| Ruta estructural | Modelo propuesto | Padre Wagtail | Hijos permitidos | Presentación/acceso público | Motivo |
|---|---|---|---|---|---|
| `/blog/` | `RouteContainerPage` | `HomePage` (`/`) | `BlogIndexPage` (`/blog/posts/`) | `live=True` como ancestro de rutas; `show_in_menus=False`; petición directa responde 404; excluir de búsquedas y sitemap | Necesario para que `/blog/posts/` y sus artículos compongan su path completo |
| `/negocio/` | `RouteContainerPage` | `HomePage` (`/`) | Cuatro `RouteContainerPage` de área | Igual: nodo técnico, no landing pública confirmada | Prefijo común de las cuatro rutas de servicio |
| `/negocio/outsourcing-bi/` | `RouteContainerPage` | `/negocio/` | `ServicePage` con slug `business-inteligence` | Igual | Segmento de jerarquía requerido por la ruta preservada |
| `/negocio/calidad-de-software/` | `RouteContainerPage` | `/negocio/` | `ServicePage` con slug `portafolio-de-servicios-qa` | Igual | Segmento de jerarquía requerido por la ruta preservada |
| `/negocio/desarrollo-de-software/` | `RouteContainerPage` | `/negocio/` | `ServicePage` con slug `fabrica-de-software` | Igual | Segmento de jerarquía requerido por la ruta preservada |
| `/negocio/gestion-documental/` | `RouteContainerPage` | `/negocio/` | `ServicePage` con slug `gestion-documental` | Igual | Segmento de jerarquía requerido por la ruta preservada |
| `/eula/` | `RouteContainerPage` | `HomePage` (`/`) | `EulaPage` (`/eula/quickbook/`) | Igual | Necesario para la ruta legal preservada |

Las páginas de destino siguen siendo las 49 del manifiesto. La tabla identifica siete ancestros estructurales fuera de esas 49; no son páginas históricas ni contenido editorial adicional. El nodo `/blog/posts/` no es estructural: es la página pública `BlogIndexPage` del manifiesto.

### 3.2 Comportamiento y restricciones

- `RouteContainerPage` será un tipo técnico mínimo, sin contenido editorial configurable; solo `title` administrativo/identificativo y slug fijo según tabla.
- Debe estar publicado en el árbol para que las rutas públicas descendientes sean resolubles. No se considera que `show_in_menus=False` proteja una página ni la vuelva privada.
- En la ruta exacta del contenedor, `serve()` debe producir 404. No debe servir una página vacía, copiar una landing no confirmada ni redirigir.
- `show_in_menus=False` evita su inclusión en menús construidos con las APIs de menú de Wagtail, pero no bloquea acceso HTTP. La búsqueda pública debe restringirse a los tipos editoriales; en sitemap, `get_sitemap_urls()` debe devolver lista vacía para estos contenedores. No inferir exclusión de búsqueda/sitemap de la propiedad de menú.
- Limitar `parent_page_types`/`subpage_types` para que cada nodo solo admita el hijo indicado. Los destinos mantienen `BlogIndexPage`, `BlogPostPage`, `ServicePage` y `EulaPage` conforme a sus relaciones permitidas.
- No se necesita un slug personalizado ni un override de `get_url_parts`: el árbol nativo representa las rutas existentes. La conducta 404 de los ancestros es el único comportamiento específico requerido.
- En FASE 1.2B, tests deben verificar cada ruta pública exacta y que cada ruta estructural directa devuelve 404; también que las páginas editoriales sean resolubles. Verificar sin usar solo `show_in_menus` como criterio de acceso.

Esta solución da la jerarquía necesaria sin afirmar que `/blog/`, `/negocio/` o `/eula/` fueran páginas públicas o destinos operativos en ProcessWire. Si posteriormente aparece evidencia de que alguno era una página pública real, revisarlo antes de alterar su comportamiento.

## 4. Almacenamiento de artículos

### 4.1 Decisión final

`BlogPostPage.body` será un **StreamField tipado**, no un campo de HTML crudo. El catálogo inicial permitirá bloques `RichTextBlock` con features explícitas y limitadas para el contenido textual. Se añadirán bloques de imagen, tabla u otros tipos solo tras confirmar que esa estructura aparece en los artículos públicos y fijar su conversión/representación. Las imágenes de cabecera y tarjeta ya confirmadas se mantienen como campo de imagen de la página; no asumir que son imágenes embebidas en el cuerpo.

La decisión prioriza edición y validación seguras sin convertir todo el cuerpo en una caja de HTML arbitrario. StreamField conserva el orden de componentes heterogéneos; RichTextBlock ofrece edición WYSIWYG acotada para cada fragmento de texto. La documentación de Wagtail advierte que StreamField no es reemplazo directo de RichTextField; aquí se elige por ser una secuencia de unidades editoriales y se limita el texto enriquecido a cada unidad, no como un campo de texto único equivalente.

### 4.2 Proceso de conversión y contenido no representable

El valor original `blog_body` es HTML que ProcessWire decodifica y el template inserta en la página. No copiarlo directamente a RichTextField/StreamField, no renderizarlo con `safe` y no asumir que el filtrado del editor equivale a sanitizar la importación.

El proceso futuro deberá:

1. Guardar temporalmente el HTML fuente en una representación de staging no renderizable (p. ej. payload de texto/JSON restringido a la herramienta de importación; no un campo público de la página).
2. Parsear con conversor controlado y allowlist de etiquetas/atributos/enlaces; validar esquemas de URL, eliminar scripts, estilos inline y elementos activos.
3. Convertir semántica reconocida a bloques tipados y RichTextBlock con features Wagtail habilitadas expresamente. Resolver links internos mediante el mapa de las 49 rutas y referencias de imágenes solo con assets aprobados.
4. Para HTML no representable (tablas complejas, embeds, atributos o estructuras desconocidas), detener la conversión de esa parte, registrar incidencia y conservar la fuente inerte para revisión. Nunca descartarla silenciosamente ni emitirla sin escapar en frontend.
5. Comparar texto visible, orden de encabezados/listas/enlaces/medios y capturas antes de aprobar. Los casos dudosos, incluidos signos `?`, requieren revisión humana, no sustitución heurística.
6. Eliminar o archivar el staging según política de retención después de resolución; no se debe volver un repositorio paralelo de contenido sensible.

### 4.3 Estado de evidencia y bloqueo

El template prueba que `blog_body` se presenta como HTML; el manifiesto y snapshots dan evidencia textual/visual. Esta fase no consultó MySQL ni recorrió los cuerpos completos para clasificar cada estructura. Por eso la elección del **tipo de almacenamiento** está cerrada, pero la lista final de bloques y features permitidos sigue pendiente de inventario representativo de los 42 artículos.

Ese pendiente **no bloquea crear el modelo vacío** `BlogPostPage` con StreamField en FASE 1.2B ni migraciones de esquema vacías. Sí bloquea importar o publicar un artículo cuyo cuerpo contenga elementos aún no representados/aprobados. La primera fase de modelos debe incluir un bloque RichText limitado y reservar extensiones tipadas; no añadir RawHTMLBlock universal.

## 5. Categorías del blog

- **Modelo:** snippet `BlogCategory`, porque se usa para clasificar y filtrar publicaciones, no se ha confirmado una ruta pública de detalle de categoría.
- **Relación:** muchos-a-muchos desde `BlogPostPage`. La auditoría confirma un campo ProcessWire de referencias múltiples y 40 asociaciones para las cinco categorías públicas; el template utiliza la relación en filtros y contenido relacionado. No imponer una sola categoría por artículo.
- **Identidad/duplicados:** `slug` único (normalizado a minúsculas y guiones ASCII para rutas internas del filtro, aunque no genere URL pública); `name` conserva etiqueta visible aprobada. Una colisión de slug debe bloquear creación y resolverse manualmente, no autoañadir sufijos que cambien identidad.
- **Orden:** campo `sort_order` explícito para preservar el orden del filtro; no depender del orden de inserción ni del orden no garantizado de una relación.
- **Allowlist:** únicamente las cinco categorías que la preservación muestra. Crear cada registro en la fase de importación solo cuando exista aprobación editorial; no generar desde referencias históricas ni etiquetas/tags.
- **Referencias no confirmadas:** relaciones a categorías históricas/tags fuera de esas cinco no se importan ni hacen fallar la creación del snippet público. El importador reportará la referencia desconocida y no la asociará por parecido de nombre.
- **Slugs:** el requisito de unicidad puede cerrarse técnicamente con restricción única. Los valores concretos de nombre/slug y las 40 asignaciones se revisan antes de importar; en esta fase no se crean categorías.

## 6. EULA

**Almacenamiento propuesto:** `EulaPage.legal_body` como `RichTextField` con allowlist de formato semántico que corresponda a la estructura comprobada en `eula.php` (encabezados, párrafos, listas, énfasis y enlaces si están presentes). No usar `RawHTMLBlock` ni una plantilla con cláusulas reescritas.

El documento actual está codificado en el template ProcessWire, no se confirmó un campo de base de datos. La importación futura debe extraer la fuente preservada, convertir únicamente etiquetas estructurales permitidas y comparar texto y orden de secciones contra la referencia exacta. No normalizar puntuación, espacios significativos, entidades o términos jurídicos automáticamente. El texto no se publica hasta revisión y aprobación legal/editorial.

La aprobación legal no bloquea crear el modelo vacío ni su migración. Sí bloquea trasladar texto al nuevo sistema, editarlo como versión vigente o publicarlo. No se propone campo de fecha/versión porque no hay evidencia suficiente de que el original mantenga ese control editorial.

## 7. Formulario Zoho: contenido frente a funcionalidad

La revisión de `contact_form.php` se limitó a identificar el comportamiento codificado; no se copiaron ni documentaron valores técnicos ocultos y no se envió el formulario.

| Área | Evidencia observada | Decisión/estado |
|---|---|---|
| Campos visibles | Nombre, Apellido, Empresa, Correo electrónico, Móvil, Mensajes y captcha; hay un campo de origen de lead no visible | El modelo de Home no almacenará datos sometidos. Si Wagtail administra texto de sección/etiquetas, solo hacerlo como configuración de presentación aprobada |
| Validación de frontend | Apellido aparece obligatorio; correo se valida por formato solo cuando tiene valor; la página incluye captcha y limita longitudes en campos visibles | No tratar validación JS como control suficiente. La futura implementación debe decidir validación servidor y accesibilidad; no inventar obligatoriedad adicional |
| Envío | El HTML define un POST directo al servicio Zoho CRM Web-to-Lead y ejecuta tracking/código del proveedor | Es integración funcional, no contenido ni campo de modelo editorial. No se copia este contrato heredado como integración nueva |
| Respuestas/estados | El formulario contiene un return target y deshabilita botón antes del envío; no se verificó la respuesta de redirección, errores, entrega, duplicados ni confirmación final | Pendiente de evidencia y definición funcional; no declarar “enviado” basándose en el template |
| Seguridad/datos | Campos incluyen PII de contacto y mensaje; captcha/seguimiento son de terceros; no hay evidencia revisada de consentimiento, retención, protección CSRF o tratamiento backend | Requiere revisión de privacidad/seguridad y decisión de integración antes de implementar envío |

**Diseño de separación:** un `ContactSectionBlock` puede representar solo elementos editoriales aprobados (título, copy y enlaces informativos). El formulario se renderizará mediante componente de frontend y servicio/adaptador de integración independiente; no se incorpora endpoint, credenciales, claves de proveedor ni datos de envíos a `HomePage`, snippets o CSV de contenido. No almacenar envíos localmente sin decisión de privacidad/retención. No hay contrato de integración autorizado en esta fase.

**Bloqueo:** modelo editorial vacío y sección visual pueden construirse; el envío real, captcha, tracking, estados de éxito/error y pruebas de envío sí están bloqueados hasta definir proveedor/arquitectura, consentimiento, antispam y comportamiento de respuesta. Nunca hacer pruebas con datos reales ni llamar a Zoho durante FASE 1.2B.

## 8. Estado de decisiones y bloqueos

| Decisión | Clasificación | Bloquea modelos vacíos en FASE 1.2B | Bloquea importación/publicación/función |
|---|---|---:|---:|
| Jerarquía con siete `RouteContainerPage` | Resuelta técnicamente | No | Tests de rutas son criterio de aceptación, no requieren DB histórica |
| `BlogPostPage.body` como StreamField | Resuelta técnicamente; inventario del catálogo de bloques pendiente de evidencia | No | Sí, si contenido contiene estructura no convertida/revisada |
| Snippet + M2M de categorías | Resuelta técnicamente | No | Sí para crear y asignar registros de producción |
| EULA como RichTextField acotado | Resuelta técnicamente | No | Sí para cargar/publicar texto sin aprobación legal |
| Formulario separado de contenido | Resuelta técnicamente | No | Sí para implementar envío o simular estado de éxito |
| Valores concretos de 5 categorías y asignaciones | Pendiente de aprobación editorial | No | Sí para importarlas |
| Texto exacto de artículos y EULA | Pendiente editorial/validación de contenido | No | Sí para importar/publicar |
| Campos visibles de contacto y política de datos | Pendiente de evidencia/aprobación | No para estructura del Home | Sí para aceptar y procesar submissions |
| Comportamiento de padres históricos ProcessWire | Pendiente de evidencia de IDs, no de path | No: el árbol Wagtail se define por las rutas preservadas | Resolver en importador si se necesita conservar IDs de padre |
| Catálogo final de bloques de blog | Pendiente de inventario de estructuras | No para iniciar el modelo vacío con bloque de texto restringido | Sí para conversión fiel de cada cuerpo complejo |

### Bloqueos reales para FASE 1.2B

No hay bloqueo técnico que impida implementar los cinco tipos editoriales vacíos, las restricciones de árbol, el StreamField inicial, el snippet/relación o la página legal sin contenido. Los siguientes límites sí deben respetarse:

1. Incluir contenedores estructurales con comportamiento directo 404 y tests de ruta; de otro modo se expondrían páginas vacías.
2. No poblar/importar ni publicar contenido/categorías/EULA sin autorización, aunque el modelo exista.
3. No renderizar HTML fuente ni implementar envío Zoho en FASE 1.2B.
4. Mantener el contrato de bloques de blog extensible y acotado; no habilitar HTML arbitrario por falta de inventario.

La falta de nombres de padres históricos no bloquea una jerarquía Wagtail que conserva URL; solo limita la correspondencia exacta de esos ancestros con IDs ProcessWire, relevante para el importador.

## 9. Criterios de aceptación de FASE 1.2B

1. Existen los cinco tipos acordados: `HomePage`, `BlogIndexPage`, `BlogPostPage`, `ServicePage`, `EulaPage`, con páginas estructurales `RouteContainerPage` separadas de contenido editorial.
2. Restricciones de padre/hijos no permiten árbol inválido; se pueden crear exactamente los segmentos necesarios para las 49 rutas.
3. Los tests calculan/consultan la URL efectiva de cada ruta del manifiesto y confirman match exacto de las 49; rutas de los siete contenedores devuelven 404 y no aparecen en navegación, búsqueda o sitemap.
4. Slugs públicos se preservan literalmente; no se traducen, transliteran ni “corrigen”.
5. `BlogPostPage.body` usa StreamField con texto enriquecido restringido; no existe bloque HTML libre ni salida insegura de la fuente ProcessWire.
6. Categorías son snippet con slug único, orden explícito y relación múltiple; no se crean categorías históricas automáticamente.
7. EULA tiene campo RichText limitado y vacío inicialmente; no se cargan ni editan términos sin revisión aprobada.
8. El modelo editorial de Home no contiene credenciales, destinos de integración inferidos ni submissions; Zoho se deja fuera de modelos y migración editorial.
9. Migraciones de esquema, si están autorizadas en esa fase, no contienen contenido importado, páginas seed ni assets históricos.
10. Sigue vigente `import_authorized=No` para las 49 rutas hasta aprobación explícita y separada.

## 10. Trazabilidad respecto del contrato 27

- La matriz de jerarquía de 27 ya no deja los padres de las rutas públicas como bloqueo técnico; esta resolución deriva siete nodos estructurales mínimos de los segmentos URL. Los IDs parent históricos continúan sin determinar y no se inventan.
- La selección de artículo se cierra en StreamField tipado más staging inerte para conversión. Se sustituye la disyuntiva abierta RichText/StreamField del documento 27, no la regla de no usar HTML crudo.
- Categorías quedan como relación M2M: el punto anterior “comprobar si una publicación puede tener más de una” se resuelve usando la relación de referencias múltiples y las asociaciones auditadas.
- EULA queda en RichTextField limitado; la aprobación legal continúa pendiente solo para el contenido/publicación.
- Contacto queda dividido entre bloque de presentación y servicio de envío por separado. No se define proveedor nuevo ni contrato de Zoho.

## Referencias técnicas

- [Wagtail 7.4: modelo Page y url_path](https://docs.wagtail.org/en/stable-7.4.x/reference/models.html)
- [Wagtail 7.4: restricciones de tipo y árbol de páginas](https://docs.wagtail.org/en/stable-7.4.x/reference/models.html#page-model)
- [Wagtail 7.4: StreamField y bloques tipados](https://docs.wagtail.org/en/v7.4/topics/streamfield.html)
- [Wagtail 7.4: RichTextBlock y RawHTMLBlock; advertencia de seguridad de RawHTMLBlock](https://docs.wagtail.org/en/stable-7.4.x/reference/streamfield/blocks.html)
- [Wagtail 7.4: Rich text internals](https://docs.wagtail.org/en/stable-7.4.x/extending/rich_text_internals.html)
- [Wagtail 7.4: snippets](https://docs.wagtail.org/en/stable-7.4.x/topics/snippets/)
- [Wagtail 7.4: PageQuerySet y páginas públicas/live](https://docs.wagtail.org/en/stable-7.4.x/reference/pages/queryset_reference.html)
- [Wagtail 7.4: sitemap y exclusión de páginas por `get_sitemap_urls()`](https://docs.wagtail.org/en/stable-7.4.x/reference/contrib/sitemaps.html)
