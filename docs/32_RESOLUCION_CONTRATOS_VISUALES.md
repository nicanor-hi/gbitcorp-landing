# 32 — Resolución de contratos visuales pendientes

**Fase:** 2.2A — análisis y documentación.

**Estado:** contratos de interacción reconciliados; se recomiendan cambios mínimos de esquema para edición completa del hero y contenido mixto de artículos, pendientes de aprobación antes de tocar modelos.

## Alcance y fuentes

Se revisaron `AGENTS.md`, `CONTEXT.md`, el manifiesto vigente, documentos 27–31, modelos/bloques Wagtail, código ProcessWire de Home/artículos, CSS/JavaScript asociado y capturas preservadas. La base histórica no se consultó en esta fase ni se modificó; se utilizan resultados documentados de las auditorías previas. El respaldo ProcessWire y `docs/reference/` permanecen de solo lectura.

El alcance permanece en las **49 rutas públicas** del manifiesto (1 Home, 1 índice, 42 artículos, 4 servicios, 1 EULA). Este análisis no autoriza a importar ni publicar esas páginas.

### Clasificación de evidencia

- **Confirmado:** legible en template/CSS/JS, modelo, manifiesto o una medición/captura preservada citada.
- **Inferido:** comportamiento de la librería según su configuración/default documentado; aún debe probarse en navegador.
- **Pendiente:** la preservación disponible no retiene la estructura/valor necesario para una conclusión por artículo o bloque.
- **Recomendación:** contrato propuesto, no implementación ni aprobación editorial.

## 1. Hero y encabezado de Home

### Evidencia observada

En `docs/gbitcorp.com/site/templates/home.php`:

- El hero es el contenedor `.banner` con fondo `site/templates/img/new/Ciudad-Fondo.png`, centrado y sin repetición en el atributo inline.
- El CSS `.banner` aplica `background-size: cover`; declara altura de 1050 px en la regla móvil y 1250 px en los rangos desde 1025 px. El contenedor del texto usa posición superior fija (`top: 23rem`) y la alineación del contenido es a la derecha. En escritorio el H1 usa 3.5 rem; en la regla móvil 3 rem; los pesos también varían por media query.
- El H1 es texto seleccionable procedente de `$page->bannerDesc`. El modelo Wagtail actual tiene `HomePage.hero_copy`, correspondencia directa con ese campo.
- El botón “CONTÁCTENOS” navega al ancla local `#contact`; etiqueta y destino están escritos en el template, no proceden del registro Home.
- Dentro de la composición de banner está el bloque “Líneas de Negocio”: encabezado y CTA “DIAGNÓSTICO GRATIS” son fijos. Cuatro links se generan al consultar servicios, traducir códigos de servicio a etiquetas fijas y apuntar al hijo de cada página. `ServiceLinksSectionBlock` ya puede guardar etiquetas y referencias a `ServicePage`, aunque el heading/CTA de sección no son editables en ese bloque.
- No se observó un slider/animación de imágenes del hero. El fondo es estático; el hover del CTA escala el botón y transiciona alrededor de 0.3 s. Una animación de botones de líneas de negocio está comentada en el footer. No se confirmó otra animación activa del hero.

En las referencias `docs/reference/home/desktop-1440x900.png`, `tablet-768x1024.png`, `mobile-390x844.png` y captura completa móvil se conserva la composición de ciudad, texto, CTA y líneas. La auditoría de rendimiento informa que la imagen de ciudad mide 3126×3909 y pesa aproximadamente 5.05 MB, y que en una captura móvil temprana el fondo todavía no aparecía. Son hallazgos de esa medición, no tiempos garantizados.

### Correspondencia y decisión

`hero_copy` representa el contenido textual variable. El recurso de fondo y ambos CTA no están en el modelo. La reproducción estática podría resolverse con una imagen versionada y labels/enlaces fijos en el template, pero dejaría el hero parcialmente fuera de la administración Wagtail y su uso de media no sería editorial.

**Recomendación mínima:** conservar `hero_copy`, añadir un único selector de imagen opcional al `HomePage` para el fondo/imagen principal y usar el asset público confirmado como valor inicial durante la carga aprobada. Mantener `#contact` y las etiquetas de CTA como constantes del template: son una acción fija de la composición, no se encontró evidencia de que cambien por página. Mantener el CTA de líneas de negocio fijo. Usar `ServiceLinksSectionBlock` para las cuatro etiquetas/destinos que actualmente están en código, con orden controlado.

**Aprobación requerida:** añadir relación a imagen modifica contrato/modelo y genera migración. Si se prefiere declarar el fondo como recurso inmutable de diseño en staticfiles, no hace falta ese campo, pero debe aprobarse que no sea editable. No añadir campos de URL/label de CTA salvo que el negocio requiera editarlos.

**Responsive recomendado:** no conservar altura rígida ni offset fijo; usar contenido para determinar la altura, `min-height` ajustable solo si la captura lo requiere, imagen adaptativa/focal point y protección de contraste. El recorte original de `cover` sobre una imagen vertical requiere comparar el focal point en los siete viewports. Priorizar la imagen solo tras confirmar que es LCP.

## 2. Carruseles que existen en Home

La inspección encontró dos carruseles activos y una inicialización huérfana de una tercera sección comentada. Se documentan separados: no son el mismo componente editorial.

### 2.1 Carrusel de imágenes de servicios (`#servicesCarousel`)

`home.php` aplana dos bucles: filas en `$page->carousel_services` y, dentro de cada fila, imágenes. Cada imagen se imprime como un `.item` con `alt="Servicios Gbit"`; no se imprime título, copy, CTA ni enlace por diapositiva. El orden es el orden de filas/imágenes de ProcessWire. La auditoría de base confirma cuatro repetidores exteriores de `carousel_services`; el número de imágenes/diapositivas no debe suponerse a partir del número de repetidores.

El modelo implementado `ServiceCarouselSectionBlock.groups -> ImageGroupBlock.images` representa precisamente esos grupos e imágenes ordenados. La correspondencia es adecuada. **La brecha de título/enlace anotada en el documento 31 fue incorrecta**: el código público no muestra esos datos en este carrusel.

Configuración explícita en `footer.php`:

| Ancho | Ítems visibles | Navegación Owl | Autoplay | Mouse drag |
|---|---:|---|---|---|
| 0–599 px | 2 | Sí | Sí, cada 5000 ms | Sí |
| 600–999 px | 3 | No | No | Sí |
| 1000 px o más | 4 | No | No | No |

El carrusel tiene `loop: true`, margen base 10 px (5 px desde 600 y 20 px desde 1000), y la captura DOM preservada registra controles/dots Owl. La auditoría responsive atribuye aproximadamente 15–16 px de overflow móvil de Home a clones fuera del viewport. El template no configura explícitamente swipe/touch; no afirmar ese comportamiento sin prueba. Los botones observados usan glifos `‹`/`›` sin nombre accesible en los metadatos preservados: corregir etiquetas y teclado al reconstruir.

### 2.2 Carrusel de equipo (`#gbircorpCarousel`)

El template itera `$page->carousel_us` y cada grupo de imágenes, dejando la primera como activa. Crea indicadores con `$page->carousel_count`; ofrece controles anterior/siguiente. Las imágenes tienen alt genérico “Colaboradores”. La auditoría SQL previa registra tres filas/repetidores de `carousel_us`, pero no se debe confundir ese número con el total de diapositivas. La captura de Home muestra carrusel en el bloque “Nosotros”.

El elemento `data-ride="carousel"`, Bootstrap 4.5.2, controles e indicadores son evidencia de carrusel cíclico iniciado al cargar. La documentación oficial de Bootstrap 4.5 indica intervalo default de 5000 ms, teclado/touch/wrap habilitados por defecto; esto último es **inferencia de default**, no una prueba de las interacciones en producción. El template no asigna explícitamente `data-interval` ni declara touch. La variable `carousel_count` y el número de imágenes deberían cotejarse para evitar indicadores sobrantes/faltantes; el modelo `AboutSectionBlock.image_groups` ya representa las imágenes ordenadas y no necesita un campo de contador redundante.

### 2.3 Carrusel de clientes: no vigente

El markup de `#customersCarousel` está comentado y la sección visible fue sustituida por “Nuestra esencia”. Aunque queda código de inicialización Owl para ese selector, no hay elemento activo en la portada preservada. **Excluirlo**; su presencia en JS legado no lo convierte en componente público actual.

### Decisión técnica

- No ampliar modelos/bloques para agregar títulos/enlaces al carrusel de servicios.
- Mantener las dos listas de imágenes actuales y su orden. Al importar, derivar slides/indicadores desde las imágenes reales y validar el conteo legacy `carousel_count`; no trasladar el contador como fuente de verdad.
- Conservar la interacción cíclica observada, pero eliminar clones que puedan escapar el viewport y proporcionar pausa/continuación accesible para autoplay, controles con nombres programáticos y soporte teclado. Respetar `prefers-reduced-motion`; si se pausa por preferencia/usuario, no reiniciar inesperadamente.
- Las imágenes actuales usan texto alternativo genérico; cada imagen importada debe recibir alt semántico o marcarse decorativa según revisión editorial. No inventar alt desde el archivo.
- Confirmar en Playwright la secuencia real, breakpoint cercano a 600/1000, pausa por foco/touch, y comportamiento de las flechas/dots antes de declarar equivalencia.

## 3. Cuerpos de los 42 artículos públicos

### Evidencia que sí está disponible

- Hay 42 rutas de plantilla `blog-post` en el manifiesto. La preservación tiene por ruta un `content.txt` con texto visible y un `page.json` de metadata/DOM resumida, además de capturas responsive. Esa evidencia conserva orden y texto visible, links/imágenes observados en el documento renderizado; no es una copia del HTML bruto de `blog_body` ni una serialización completa del DOM semántico.
- `docs/gbitcorp.com/site/templates/blog-post.php` emite `html_entity_decode($page->blog_body)` directamente dentro de `.article_body`. No hay en esa salida un sanitizador explícito. El template muestra compartir antes/después del cuerpo y hasta cuatro relacionados bajo el cuerpo; al auditar layout hay que separar esos componentes del body real.
- El modelo actual `BlogPostPage.body` solo admite un tipo StreamField `rich_text`, con funciones `h2`, `h3`, `h4`, `bold`, `italic`, `ol`, `ul`, `link`. No permite imágenes ni tablas. Tampoco ofrece campos explícitos para caption/alineación.
- `docs/12_PROBLEMAS_RESPONSIVE.md` identifica imágenes de contenido con clases `align_left`/`align_right` y dimensiones intrínsecas grandes; las rutas `smartqa-una-iniciativa-gbit`, `error-defecto-y-fallo` e `implementar-la-digitalizacion-masiva-de-documentos` son ejemplos con overflow móvil de hasta 689, 617 y 646 px respectivamente a 390 px. A 1024 px se registraron imágenes de 992–1064 px que excedían el contenedor.
- El mismo informe documenta una tabla pegada desde documentos con clase `MsoTableGrid`, ancho de 800 px, en el artículo `moneyball-el-arte-de-ganar-un-juego-injusto`; en 390 px excede 431 px. Esto confirma al menos una tabla pública con formato rígido, no el total de tablas en los 42 cuerpos.
- El template original aplica `html_entity_decode` una vez. La auditoría de codificación `docs/20` confirma conversión de charset en muestras, y recomienda sanitización allowlist, sin redecodificación global. Los signos `?` literales confirmados no deben “corregirse” automáticamente.

### Qué no puede concluirse de la preservación actual

Los `page.json` y las capturas no incluyen el HTML fuente de los 42 campos. Las listas de imágenes y anchors de página completa mezclan contenido con header, botones sociales, relacionados y footer y no sirven como inventario del cuerpo. La FASE 2.2A.1 consultó únicamente `field_blog_body` para los 42 IDs públicos mediante `pw_auditor` y documentó el resultado por ID/ruta en `docs/33_AUDITORIA_HTML_ARTICULOS.md`, sin almacenar cuerpos HTML.

En el HTML fuente se contabilizaron **12 tags `<table>` en cinco artículos**, 37 imágenes de cuerpo en 17 artículos y 28 enlaces. Cuatro tablas tienen clase `MsoTableGrid`; ninguna etiqueta `<th>`, `<caption>`, `rowspan` o `colspan` fue detectada por el parser. Treinta y siete imágenes tienen `alt=""`; la intención decorativa frente a falta de texto alternativo no puede deducirse automáticamente. Estos son conteos sintácticos del campo, no clasificación semántica: el parser estándar empleado no reconstruye el DOM HTML5 y las tablas no-Mso pueden ser layout o contenido. Filas/columnas reportadas son observaciones tokenizadas, no evidencia suficiente de la semántica final. No se detectaron `<figure>`/`<figcaption>`.

### Contrato recomendado para StreamField

1. Conservar RichText como bloque de texto con allowlist actual y orden intercalable.
2. Añadir un bloque tipado de imagen dentro de la secuencia. Usar el control de imagen Wagtail que captura alt o decoración; incluir caption solo si la inspección del cuerpo confirma captions editoriales. Puede haber una alineación explícita limitada si hace falta preservar una imagen alineada en escritorio; en tablet/móvil debe colapsar a imagen fluida sin float/overflow. No inferir caption desde texto vecino.
3. Añadir soporte de tabla únicamente a partir de las tablas públicas semánticas identificadas. Hay evidencia de al menos una tabla ancha, por lo que la capacidad parece necesaria para fidelidad, pero su tipo definitivo depende de inspeccionar celdas/encabezados. Para una tabla simple de texto evaluar el TableBlock contrib de Wagtail 7.4 (con campo caption); para celdas tipadas con RichText/imágenes evaluar TypedTableBlock o un bloque propio mínimo. No habilitar contenido HTML crudo.
4. Envolver tablas anchas en contenedor con overflow horizontal local, foco/teclado y nombre/ayuda accesible; preferir reflujo por filas solo si conserva relaciones de encabezados y comprensión. Mantener `<caption>`, `<th>` y scope/headers cuando la semántica fuente lo soporte. No convertir tabla de datos en tarjetas sin revisión editorial.
5. Preservar enlaces en RichText con URL normalizada; resolver rutas internas contra el manifiesto. Si un link envuelve una imagen, conservar esa relación solo si se confirma en el body original y validar destino permitido.

**Cambio mínimo probable en FASE 1.2D/2.2B (nombre de fase por acordar):** extender `BlogPostPage.body` con `image` y `table`, conservar `rich_text`; no agregar campos separados por cada estructura ni reinstalar toda la página como HTML. Esto cambia esquema de StreamField y requiere migración compatible/revisada, pruebas de serialización y aprobación antes de ejecutar. No se efectuó aquí.

### Sanitización y transformación para el importador

- Leer solo las filas A del manifiesto y los recursos B que realmente sirven a sus cuerpos. Mantener la relación página/ID original/ruta, secuencia y referencias de asset.
- Convertir charset latin1/CP1252 a Unicode una sola vez conforme a `docs/20`; decodificar entidades HTML exactamente una vez, porque el template legado lo hace una vez. Probar texto con tildes, ñ, entidades y `?` literales; no corregir por heurística.
- Parsear el HTML con parser y allowlist explícita en vez de imprimir `blog_body` como HTML seguro. Aceptar solo los elementos editoriales previstos (párrafos, h2–h4, strong/em, listas, enlaces y estructura explícita de imágenes/tablas). Eliminar scripts, estilos inline arbitrarios, event handlers, iframes/forms, elementos activos y atributos desconocidos.
- Permitir solo esquemas de enlace aprobados (`https`, `http`, `mailto`, `tel` y relativos internos validados); rechazar `javascript:`, `data:` y destinos no autorizados. Normalizar enlaces externos y decidir `rel`/`target` según política común, no copiarlos ciegamente.
- Mapear imágenes locales de ProcessWire a media autorizada en Wagtail, confirmar archivo existente y asociación a ruta. No importar remotos o los 728 assets completos. Mantener alt/caption como dato explícito; faltantes o ambiguos generan revisión, no texto inventado.
- Para tablas reconocer estructura de filas/columnas/encabezados, detectar `rowspan`/`colspan`, links e imágenes en celdas y anchos fijos; si el bloque no puede representarla, detener ese registro para revisión. Eliminar anchos/estilos de Word solo durante una conversión estructurada aprobada, nunca con `replace` ciego en HTML.
- Registrar errores por ID/ruta y tipo de conversión, no volcar contenido personal, cuerpos HTML, credenciales ni la fila completa en logs. Mantener staging inerte y preview hasta aprobación editorial; no publicar automáticamente.
- Sanitizar salida/render además de validar entrada; los bloques StreamField no se deben tratar como sanitizador general de datos HTML arbitrarios.

## 4. Matriz de decisiones

| Brecha | Evidencia original | Modelo/bloque actual | Diferencia | Recomendación y cambio mínimo | Riesgo/aprobación |
|---|---|---|---|---|---|
| Hero Home | `home.php` background city + `bannerDesc` + anchor CTA; CSS `cover`, alturas rígidas | `HomePage.hero_copy`; no image field | Texto mapeado; fondo no editable en Wagtail | Recomendar 1 FK de imagen opcional; CTA y línea visual permanecen fijos; reutilizar `service_links` para los cuatro destinos | Requiere aprobación de cambio de modelo/migración o aprobación explícita de asset estático no editable. |
| Carrusel servicios | 4 grupos outer auditados; PHP emite imágenes ordenadas, sin copy/link; opciones Owl breakpoint-specific | `ServiceCarouselSectionBlock.groups` / `ImageGroupBlock.images` | No hay brecha de datos; discrepancia anterior de doc31 corregida | Sin cambios de modelo; implementar como carrusel accesible sin clones, alt por media, controles nombrados | Interacciones exactas y touch deben verificarse; cambios accesibilidad de comportamiento son recomendados. |
| Carrusel equipo | `carousel_us`; indicators dependen de `carousel_count`; controls prev/next; `data-ride` | `AboutSectionBlock.image_groups` | Lista imágenes coincide; counter redundante/no incluido | Sin contador de esquema; derivar indicadores de slides reales y cotejar al importar | Requiere revisión si conteo fuente no coincide. Autoplay necesita pausa y `prefers-reduced-motion`. |
| Carrusel clientes | Markup comentado; no visible en capture actual | Sin bloque activo | Código/init huérfano | Excluir sin contenido/modelo | No requiere aprobación para excluir lo no público confirmado. |
| Imágenes de artículo | imágenes de cuerpo/alineaciones y overflow identificados en informe 12 | RichTextBlock sin feature de imagen | No representación tipada ni alt por cuerpo | Añadir bloque de imagen en StreamField; alignment acotado solo si captura lo requiere, colapsa en móvil | Requiere cambio de esquema y revisión de alt; caption/link quedan pendientes de evidencia. |
| Tablas de artículo | Al menos una `MsoTableGrid` 800px; exact count y semántica pendientes | RichTextBlock no admite tablas | Estructura rígida no se puede migrar a block actual | Auditar HTML seguro de los 42 A; TableBlock para tablas simples confirmadas; typed/custom solo si la estructura exige celdas ricas | Requiere aprobación de bloque/migración y decisión editorial sobre tablas de layout/merges. |
| Enlaces/HTML | `html_entity_decode()` una vez + echo directo | RichText allowlist limitada | Enlaces/etiquetas pueden exceder allowlist y raw HTML sería inseguro | parser+allowlist, convertir links/bloques, no renderizar source sin sanitizar | La conversión puede cambiar formato; fallos van a revisión, no a publicación. |

## 5. Decisiones confirmadas y pendientes

### Confirmadas

- Hero: `bannerDesc` corresponde a `hero_copy`; los CTA/anclas son constantes visibles en el template; fondo es imagen estática con `cover`; no hay slider de hero observado.
- La línea de negocio dentro del banner está generada desde servicios y etiquetas en PHP; el modelo `service_links` puede representar los vínculos si se conserva el orden y las etiquetas.
- Carrusel de servicios = imágenes, sin título/link. `ServiceCarouselSectionBlock` coincide con la fuente; no se requiere ampliar ese bloque.
- Hay un segundo carrusel de equipo y no debe mezclarse con el de servicios. El carrusel de clientes ya no está en la página pública.
- Cuerpo del artículo StreamField no cubre imágenes ni tablas; hay evidencia pública de ambos tipos y del overflow resultante.
- El HTML original se decodifica por entidad una vez y se imprime directamente; no se debe migrar como HTML confiable.
- El manifiesto y URLs no cambian; contenido histórico no se incorpora.

### Pendientes de aprobación/evidencia

1. Aprobar o rechazar `HomePage.hero_image` (una imagen controlada por Wagtail) frente a fondo estático no editable.
2. Revisar relación real entre cantidad de `carousel_count` e imágenes de equipo al importar; confirmar intervalos/gestos de carruseles con Playwright antes de fijar interacción.
3. **Realizado parcialmente en 2.2A.1:** se cuenta la estructura sintáctica de los 42 `blog_body` en `docs/33`. Pendiente: validar HTML5/DOM y clasificar las tablas de los cinco artículos como datos vs. layout; decidir significado de `alt=""`; confirmar relaciones de enlace/imagen y comprobar filas/columnas de tablas potencialmente malformadas.
4. Aprobar extensión mínima de StreamField con `image` y `table` después de clasificar estructuras. No se debe bloquear templates generales confirmados, pero sí la carga y presentación final de posts que requieran estructura no representable.
5. Determinar si se requiere dependencia/configuración adicional para el bloque de tabla contrib seleccionado; hacer compatibilidad con Wagtail 7.4.4 sin instalar en FASE 2.2A.

La revisión del HTML de artículo puede hacerse posteriormente con acceso de solo lectura restringido a las 42 rutas A, evitando tablas sensibles, comentarios, usuarios, sesiones y submissions. No utilizar datos distintos del manifiesto.

## 6. Plan de implementación posterior

1. Obtener decisión editorial sobre administración de la imagen de hero; si se aprueba, hacer modificación acotada del contrato/modelo y migración antes de template Home. Si no, incorporar asset como staticfile versionado solo tras autorización de selección.
2. Corregir modelo de carruseles solo si la auditoría de conteos revela una incompatibilidad real; no añadir títulos, links o counter por anticipado.
3. Revisar los 42 HTML públicamente confirmados en modo read-only y generar una matriz estructural redactada: por ruta, conteo/tipo de imagen/tabla, align/alt/caption/link y estado. No guardar cuerpos completos.
4. Confirmar requerimientos del bloque de tabla y actualizar contract 27/28/29 antes de schema changes. Agregar `ImageBlock` y el mínimo bloque de tabla con allowlist/validación, pruebas y migración revisada.
5. Implementar un conversor de staging no publicable: HTML parser, reglas versionadas, charset/entidades una vez, allowlist, conversión de imágenes/tablas/enlaces y reporte de errores no sensible.
6. Crear previews Wagtail para casos representativos y revisar con editor las 49 rutas candidatas; no publicar/importar sin aprobación editorial.
7. Construir templates de hero, links y ambos carruseles, completar labels/ARIA/pausa/reduced motion, responsive sin alturas/clones problemáticos.
8. Probar secuencia de slides, indicadores, teclado, touch real si soportado, 7 viewports y comparación visual contra capturas preservadas; no enviar formularios.

## Criterio de cierre 2.2A

La brecha del carrusel de servicios queda **resuelta sin cambio de modelo**; la del equipo queda definida sin contador duplicado. El contrato visual del hero tiene solución mínima propuesta pero requiere aprobación de su condición editable. Los artículos tienen un modelo destino recomendado, pero faltan datos detallados de HTML para fijar el bloque de tabla y convertir/importar cuerpo. Esta fase no inicia frontend ni importación.

## Referencias locales y oficiales

- `docs/gbitcorp.com/site/templates/home.php`, `footer.php`, `css/new/main.css`.
- `docs/reference/home/page.json`, `content.txt`, capturas desktop/tablet/móvil y auditoría `docs/12_PROBLEMAS_RESPONSIVE.md`, `docs/14_DIAGNOSTICO_HOME_RENDIMIENTO.md`.
- Artículos: `docs/gbitcorp.com/site/templates/blog-post.php`; manifiesto `docs/21_MANIFIESTO_CONTENIDO_VIGENTE.csv`; capturas/meta por ruta en `docs/reference/blog/posts/`; auditoría `docs/20_VALIDACION_CODIFICACION.md`.
- Modelos/bloques: `editorial/models.py`, `editorial/blocks.py`; contrato `docs/27_` y `docs/28_`; implementación `docs/29_`; validación `docs/30_`.
- [Wagtail 7.4 StreamField para contenido mixto](https://docs.wagtail.org/en/v7.4/topics/streamfield.html), [bloques Wagtail 7.4](https://docs.wagtail.org/en/stable-7.4.x/reference/streamfield/blocks.html), [Wagtail contrib TableBlock](https://docs.wagtail.org/en/v7.4/reference/contrib/table_block.html), [Typed Table Block](https://docs.wagtail.org/en/v7.4/reference/contrib/typed_table_block.html).
- [Bootstrap 4.5 Carousel](https://getbootstrap.com/docs/4.5/components/carousel/) (default de 5000 ms, data-ride, keyboard, touch y wrap; aplicado como inferencia de versión/default, no como prueba de gesto en el sitio público).
