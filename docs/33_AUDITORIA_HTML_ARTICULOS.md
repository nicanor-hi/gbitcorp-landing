# 33 — Auditoría estructural del HTML de artículos públicos

**Estado:** inspección de solo lectura completada para los 42 artículos A del manifiesto. No se convirtió ni modificó contenido.

## Alcance y método

- Fuente editorial: las 42 filas `A - Public confirmed` con template `blog-post` de `docs/21_MANIFIESTO_CONTENIDO_VIGENTE.csv` (IDs y rutas se listan en la matriz). No se seleccionaron otras páginas.
- Fuente de estructura: campo `field_blog_body` de la restauración local `processwire_gbitcorp_local`, consultado únicamente mediante `pw_auditor` en `127.0.0.1:3307`. La consulta fue `SELECT` restringido a esos 42 IDs; el cuerpo se convirtió a UTF-8 en la sesión y se transportó solo en memoria al parser. No se guardaron cuerpos ni credenciales en el repositorio.
- El parser Python estándar `html.parser` contabilizó etiquetas, atributos seleccionados, clases y relaciones sintácticas básicas entre `table`, `tr`, `td` y `th`. El reporte temporal contiene solo ID/ruta y métricas y está fuera del repositorio.
- La extracción no es un parser HTML5 con recuperación del DOM del navegador. Los conteos de etiquetas de apertura son reproducibles para el campo; filas/celdas y geometría son evidencia sintáctica, no prueba definitiva de cómo el navegador repara HTML inválido. Antes de fijar un bloque de tabla, validar los cinco casos con DOM/renderizado o revisión controlada de su estructura, sin volcar los cuerpos a documentación.

## Resumen de resultados

En los 42 cuerpos se detectaron:

- 12 etiquetas `<table>` en cinco artículos: ID 1080 (4), 1641 (1), 1667 (2), 1669 (1) y 1670 (4). Cuatro llevan clase `MsoTableGrid`; dos tienen ancho fijo detectado. El parser no observó `th`, `caption`, `rowspan` ni `colspan`. Esto no permite todavía clasificar todas las tablas como datos o maquetación.
- 37 etiquetas `<img>` distribuidas en 17 artículos; todas traen atributo `alt` vacío (`alt=""`), ninguna omite el atributo y ninguna tiene texto alternativo no vacío. Esto puede representar decoración o falta editorial; la intención no queda probada. Treinta y cinco imágenes incluyen atributo `width`; ninguna tiene atributo HTML `align` ni aparece envuelta por una etiqueta `<a>` en el cuerpo consultado. Deben revisarse dimensiones/alineación CSS al convertir.
- 15 ocurrencias de clases de alineación (`align_left`/`alignleft`: 8; `align_right`/`alignright`: 7) en siete artículos. El parser cuenta la clase en cualquier elemento, no solo en `<img>`; las capturas y `docs/12_PROBLEMAS_RESPONSIVE.md` ya evidencian desbordamiento de imágenes alineadas.
- 28 enlaces `<a>`; no se detectaron esquemas `javascript:`, `data:` o `vbscript:` en sus `href`. Esto no sustituye la validación de destinos contra el manifiesto al importar.
- 92 encabezados: h2=43, h3=40, h4=5, h5=4. Listas: 43 `<ul>`, 9 `<ol>` y 243 `<li>`. También se detectaron un `<blockquote>` y cuatro `<hr>`.
- No se detectaron `<figure>`, `<figcaption>`, `<iframe>`, `<video>`, `<audio>`, `<object>`, `<embed>`, `<script>`, `<style>` ni `<form>` en estos campos.

Los campos de imágenes independientes de ProcessWire (por ejemplo `blog_images`) no forman parte de estas cifras: la matriz cuenta exclusivamente `<img>` presente dentro de `blog_body`.

## Matriz por artículo

`Tabla` muestra cantidad de etiquetas y el resultado sintáctico filas × columnas del parser. “—” indica que no se encontró esa etiqueta, no ausencia de contenido textual. Los encabezados/listas/enlaces son conteos de etiquetas, no conteos de secciones visuales. `Validación` se refiere a extracción y asociación con la fila A; la clasificación semántica y editorial de tablas/alt sigue pendiente.

| ID | Ruta pública | Tablas (tags; filas × columnas observadas) | Imágenes en body | Otras estructuras detectadas | Riesgo / requisito editorial | Validación |
|---:|---|---|---:|---|---|---|
| 1045 | `/blog/posts/example-post/` | — | 0 | h2=1, h3=2 | Contrastar orden y texto contra captura antes de convertir | SQL y ruta A confirmados; estructura extraída |
| 1057 | `/blog/posts/new-post-test/` | — | 0 | h2=1 | Contrastar orden y texto contra captura antes de convertir | SQL y ruta A confirmados; estructura extraída |
| 1063 | `/blog/posts/nuevo-articulo/` | — | 0 | h2=1, h3=7; ul=1, li=5 | Mantener listas y jerarquía de encabezados en RichText permitido | SQL y ruta A confirmados; estructura extraída |
| 1076 | `/blog/posts/implementar-la-digitalizacion-masiva-de-documentos/` | — | 1 | h2=1, h3=4; ul=4, li=12; img con `width` | Alt vacío por clasificar; quitar dependencia de ancho rígido | SQL y ruta A confirmados; estructura extraída |
| 1078 | `/blog/posts/como-compartir-documentos-electronicos-dentro-de-la-organizacion/` | — | 0 | h2=1 | Contrastar orden y texto contra captura antes de convertir | SQL y ruta A confirmados; estructura extraída |
| 1080 | `/blog/posts/como-asegurarse-que-los-servicios-de-cloud-computing-sean-eficientes/` | 4; cada una 1×1 | 2 | h2=1, h5=2; imágenes con `width` | Posibles tablas de una celda/maquetación; clasificar estructura antes de crear TableBlock; revisar alt | SQL y ruta A confirmados; semántica de tablas pendiente |
| 1086 | `/blog/posts/green-it-piensa-verde/` | — | 4 | h2=1, h3=2, h4=1; imágenes con `width` | Alt vacío por clasificar; quitar dependencia de ancho rígido | SQL y ruta A confirmados; estructura extraída |
| 1088 | `/blog/posts/cuando-mantener-tus-documentos-por-siempre-no-es-una-opcion/` | — | 0 | h2=1, h3=1 | Contrastar orden y texto contra captura antes de convertir | SQL y ruta A confirmados; estructura extraída |
| 1090 | `/blog/posts/el-desafio-de-la-licitacion-electronica-en-el-sector-publico/` | — | 1 | h2=1 | Alt vacío por clasificar | SQL y ruta A confirmados; estructura extraída |
| 1091 | `/blog/posts/hablemos-sobre-la-gestion-de-contenidos/` | — | 1 | h2=1; ul=1, li=6 | Alt vacío por clasificar; preservar lista | SQL y ruta A confirmados; estructura extraída |
| 1254 | `/blog/posts/error-defecto-y-fallo/` | — | 3 | h2=4, h3=2, h4=1; ul=4, li=10; a=4; align-right=2; imágenes con `width` | Validar orden de enlaces e imágenes; convertir alineación a layout fluido; alt por revisar | SQL y ruta A confirmados; estructura extraída |
| 1259 | `/blog/posts/que-es-inteligencia-de-negocios/` | — | 4 | h2=2, h3=6, h4=1; ul=2, li=13; a=5; imágenes con `width` | Revisar alt y destinos; preservar listas/jerarquía | SQL y ruta A confirmados; estructura extraída |
| 1273 | `/blog/posts/las-pruebas-de-experiencia-de-usuario-ux/` | — | 1 | h2=4, h4=1, h5=2; ul=1, ol=1, li=6; a=3 | Revisar alt y enlaces; h5 no está incluido en la lista actual de RichText aprobada | SQL y ruta A confirmados; estructura extraída |
| 1276 | `/blog/posts/tips-para-identificar-un-correo-phishing/` | — | 3 | h2=1, h3=1, h4=1; a=4; blockquote=1; imágenes con `width` | Preservar cita como estructura semántica; alt y enlaces por validar | SQL y ruta A confirmados; estructura extraída |
| 1319 | `/blog/posts/business-intelligence-o-big-data/` | — | 0 | Sin encabezados/listas/enlaces especiales detectados | El extractor no determina si la estructura es solo párrafos; cotejar texto visible | SQL y ruta A confirmados; estructura extraída |
| 1322 | `/blog/posts/componentes-de-origen-de-datos/` | — | 0 | h2=1; a=2 | Validar destinos y formato permitido de enlaces | SQL y ruta A confirmados; estructura extraída |
| 1323 | `/blog/posts/qu-son-las-pruebas-de-automatizacin/` | — | 0 | h2=3; ul=4, li=14 | Preservar el orden de listas | SQL y ruta A confirmados; estructura extraída |
| 1325 | `/blog/posts/top-10-herramientas-para-pruebas-automatizadas/` | — | 0 | h2=1, h3=10; ul=6, li=44 | Mantener anidamiento/orden de listas; confirmar profundidad, no medida por conteo simple | SQL y ruta A confirmados; estructura extraída |
| 1327 | `/blog/posts/test-complete/` | — | 0 | h2=1, h3=3; ul=4, li=41 | Mantener anidamiento/orden de listas; confirmar profundidad | SQL y ruta A confirmados; estructura extraída |
| 1349 | `/blog/posts/inteligencia-de-negocios-en-marketing-de-contenido/` | — | 0 | h3=1; a=2; ul=4, li=9 | h3 sin h2 detectado; revisar jerarquía visual y enlaces | SQL y ruta A confirmados; estructura extraída |
| 1527 | `/blog/posts/tecnologia-impulsada-por-la-salud/` | — | 0 | h2=1; a=2; ol=2, li=3 | Revisar destinos y preservar orden de lista | SQL y ruta A confirmados; estructura extraída |
| 1619 | `/blog/posts/el-reto-tecnologico-que-nos-trajo-el-covid-19/` | — | 0 | h2=1 | Contrastar orden y texto contra captura antes de convertir | SQL y ruta A confirmados; estructura extraída |
| 1633 | `/blog/posts/vision-del-futuro-para-el-area-de-calidad-y-pruebas-de-software/` | — | 0 | h2=1; a=1 | Validar destino del enlace | SQL y ruta A confirmados; estructura extraída |
| 1641 | `/blog/posts/smartqa-una-iniciativa-gbit/` | 1; 1×3, `MsoTableGrid`, ancho fijo | 3 | h2=1; imágenes con `width` | Confirmar si tabla es de datos o layout; no hay th/caption/merges detectados; alt por revisar | SQL y ruta A confirmados; semántica pendiente |
| 1657 | `/blog/posts/la-inteligencia-artificial-en-el-e-commerce/` | — | 0 | h2=1 | Contrastar orden y texto contra captura antes de convertir | SQL y ruta A confirmados; estructura extraída |
| 1666 | `/blog/posts/nuestra-propuesta-e-commerce-vitrina-360/` | — | 0 | h2=1 | Contrastar orden y texto contra captura antes de convertir | SQL y ruta A confirmados; estructura extraída |
| 1667 | `/blog/posts/una-app-para-tu-negocio-considera-una-pwa-entre-tus-opciones/` | 2; ambas 2×2, `MsoTableGrid` | 0 | h2=1; a=2; ul=4, ol=3, li=29; anchos fijos en elementos | Clasificar ambas tablas; confirmar si son datos y si la estructura de celdas refleja DOM; revisar enlaces/estilos Word | SQL y ruta A confirmados; semántica pendiente |
| 1668 | `/blog/posts/servicios-de-gestion-documental/` | — | 0 | h2=1; ul=1, li=10 | Preservar lista | SQL y ruta A confirmados; estructura extraída |
| 1669 | `/blog/posts/moneyball-el-arte-de-ganar-un-juego-injusto/` | 1; 1×3, `MsoTableGrid`, ancho fijo | 1 | h2=1; a=1; imagen con `width` | Evidencia responsive previa registra tabla de 800 px; clasificar semántica y eliminar ancho rígido sin perder relaciones de celdas | SQL y ruta A confirmados; semántica pendiente |
| 1670 | `/blog/posts/smart-control-sistema-de-marcacion-y-control-de-esfuerzo/` | 4; cada una 1×2 | 4 | h2=1; align-left=4; imágenes con `width` | Probables tablas de layout asociadas a imágenes, aún no confirmado; no convertir como tablas de datos por defecto; alt/alineación por revisar | SQL y ruta A confirmados; semántica pendiente |
| 1722 | `/blog/posts/herramienta-bi-para-el-analisis-y-captador-de-oportunidades-en-la-plataforma-chile-compra/` | — | 0 | h2=1 | Contrastar orden y texto contra captura antes de convertir | SQL y ruta A confirmados; estructura extraída |
| 1723 | `/blog/posts/virtual-pedigree-consultant-of-classic-grade-winners/` | — | 2 | h2=1; align-left=1, align-right=1; imágenes con `width` | Resolver alt; eliminar floats rígidos manteniendo intención visual | SQL y ruta A confirmados; estructura extraída |
| 1724 | `/blog/posts/modelo-cmmi/` | — | 2 | h2=1, h3=1; a=2; ul=4, li=21; align-left=1, align-right=1; imágenes con `width` | Resolver alt; adaptar alineaciones a móvil; validar destinos | SQL y ruta A confirmados; estructura extraída |
| 1725 | `/blog/posts/programa-de-profesionalizacion-gbit/` | — | 1 | h2=1; align-right=1; imagen con `width` | Resolver alt; adaptar alineación | SQL y ruta A confirmados; estructura extraída |
| 1726 | `/blog/posts/los-esfuerzos-de-panama-por-convertirse-en-una-ciudad-inteligente/` | — | 2 | h2=1; align-left=1, align-right=1; imágenes con `width` | Resolver alt; adaptar alineaciones a móvil | SQL y ruta A confirmados; estructura extraída |
| 1727 | `/blog/posts/gobernanza-y-uso-estrategico-de-datos-en-el-sector-publico-panameno/` | — | 2 | h2=1; ul=3, li=9; align-left=1, align-right=1; imágenes con `width` | Resolver alt; preservar listas y adaptar alineaciones | SQL y ruta A confirmados; estructura extraída |
| 1767 | `/blog/posts/la-busqueda-de-la-confianza-digital-el-nacimiento-de-blockchain/` | — | 0 | Sin encabezados/listas/enlaces especiales detectados | El extractor no determina si la estructura es solo párrafos; cotejar texto visible | SQL y ruta A confirmados; estructura extraída |
| 1786 | `/blog/posts/tecnologas-emergentes-que-estn-redefiniendo-el-futuro/` | — | 0 | Sin encabezados/listas/enlaces especiales detectados | El extractor no determina si la estructura es solo párrafos; cotejar texto visible | SQL y ruta A confirmados; estructura extraída |
| 1787 | `/blog/posts/el-rol-del-internet-de-las-cosas-iot-en-la-transformacin-digital/` | — | 0 | ol=1, li=3 | Preservar orden de lista | SQL y ruta A confirmados; estructura extraída |
| 1788 | `/blog/posts/la-revolucin-de-la-inteligencia-artificial-en-los-negocios/` | — | 0 | Sin encabezados/listas/enlaces especiales detectados | El extractor no determina si la estructura es solo párrafos; cotejar texto visible | SQL y ruta A confirmados; estructura extraída |
| 1789 | `/blog/posts/la-importancia-del-big-data-en-la-toma-de-decisiones-empresariales/` | — | 0 | ol=1, li=4 | Preservar orden de lista | SQL y ruta A confirmados; estructura extraída |
| 1791 | `/blog/posts/el-futuro-de-la-computacin-cuntica/` | — | 0 | ol=1, li=4 | Preservar orden de lista | SQL y ruta A confirmados; estructura extraída |

## Ejemplos representativos y contraste público

- **Tablas con formato de Word:** IDs 1641, 1667 (dos) y 1669 tienen cuatro tags `MsoTableGrid`. El informe visual previo documenta en `moneyball-el-arte-de-ganar-un-juego-injusto` una tabla de ancho fijo de 800 px que excede el viewport móvil. En el HTML tokenizado aparecen 3 celdas en los casos de 1641 y 1669 y dos filas por dos columnas en cada tabla de 1667. No hay celdas `<th>`, caption ni fusiones detectadas; los valores no se copiaron al informe.
- **Posibles tablas de layout:** ID 1080 contiene cuatro tablas de una celda/una fila; ID 1670 cuatro de dos celdas/una fila. Son candidatas a maquetación, no se declara que lo sean sin inspección semántica. En 1670 también hay cuatro ocurrencias `align_left` y las cuatro imágenes tienen `width`.
- **Imágenes alineadas:** IDs 1254, 1723–1727 muestran clases de alineación dentro del cuerpo; 1254 corresponde también al ejemplo de imagen que desborda hasta 617 px de ancho total a viewport 390 en `docs/12_PROBLEMAS_RESPONSIVE.md`. Las clases no equivalen necesariamente una a una a imágenes.
- **Estructuras textuales:** el conjunto usa h2–h5, listas ordenadas/no ordenadas, enlaces y una cita. Un bloque RichText restringido sigue cubriendo texto común, pero los h5 observados requieren decisión: enriquecer allowlist o mapear semánticamente a nivel admitido con revisión, no degradarlo silenciosamente.

## Comparación con bloques actuales y propuesta mínima

`BlogPostPage.body` permite actualmente solo `rich_text`, con funciones `h2`, `h3`, `h4`, `bold`, `italic`, `ol`, `ul`, `link` (`editorial/models.py`). La auditoría confirma necesidades de contenido mixto:

1. **Conservar RichText restringido** para texto, encabezados admitidos, listas y enlaces. Revisar h5: aparece en artículos 1080 y 1273 y no está hoy en la allowlist.
2. **Bloque `ImageBlock` tipado** para los 37 `<img>` inline, con referencia a media y alt/decoración editorial. No importar ni asociar automáticamente estos recursos. Solo añadir caption/alineación/enlace al contrato si revisión puntual confirma esos datos; las fuentes inspeccionadas no tienen `figure`/`figcaption` y no usan atributo HTML `align`.
3. **No cerrar todavía el diseño de `TableBlock`.** Hay 12 tags, pero falta clasificar las ocho tablas no `MsoTableGrid` como datos o layout y verificar el DOM efectivo de las tablas Word. No se observaron cabeceras semánticas ni merges; si la revisión confirma tablas de datos simples, evaluar un TableBlock tipado mínimo con encabezado/caption solo si la fuente lo requiere. Las tablas de layout deben convertirse a composición HTML/CSS, no conservarse como tablas editoriales. No habilitar HTML crudo.
4. La cita en ID 1276 no tiene bloque StreamField actual explícito. Confirmar si el contenido requiere `<blockquote>` semántico antes de decidir un bloque de cita o transformación revisada a RichText.

Estos hallazgos no autorizan una migración de contenido ni una alteración de modelos. Todo cambio de StreamField requiere fase aprobada, contrato actualizado, pruebas y migración de esquema revisada.

## Sanitización para el futuro importador

La extracción no implementa sanitización. El conversor futuro debe ser un parser estructural con transformaciones explícitas; nunca renderizar el HTML heredado directamente ni confiar en una lista de sustituciones de cadenas.

- **Codificación y entidades:** recuperar latin1/CP1252 según columna verificada y convertir a Unicode una sola vez. Aplicar decodificación de entidades como lo hace el template solo una vez. No “arreglar” mojibake o signos `?` mediante heurísticas.
- **Etiquetas:** allowlist concreta alineada con bloques aprobados: párrafo, h2–h4 (h5 pendiente), énfasis, listas y anchors; `<img>` y `<table>` solo tras mapeo a bloque tipado. `<blockquote>` requiere decisión. Eliminar scripts, estilos, formularios, iframes, embeds y elementos desconocidos/activos.
- **Atributos:** conservar solo campos tipados (alt/decoración, caption aprobada, alineación editorial limitada, encabezados y relaciones de tabla verificadas, clase semántica aprobada). Eliminar atributos `on*`, estilos inline arbitrarios, anchos/altos rígidos y atributos desconocidos; no se extraen como dato editorial automáticamente.
- **Enlaces:** aceptar `https`, `http`, `mailto`, `tel` y rutas relativas solo tras validación; comparar internos con el manifiesto y clasificar los demás como externos/especiales. Rechazar `javascript:`, `data:`, `vbscript:` y protocolos no aprobados; mantener URL, origen y decisión en el reporte no sensible.
- **Imágenes:** mapear únicamente archivo local probado contra la referencia del artículo; no seguir ni descargar destinos externos. El atributo `alt=""` no permite decidir decoración vs. falta editorial: bloquear publicación del bloque hasta resolver ese dato con criterio editorial/accesible.
- **Tablas:** distinguir datos de layout; conservar filas/celdas y encabezados solo con semántica demostrada. Detectar `rowspan`/`colspan`, encabezados, enlaces/imágenes de celda, celdas vacías y estilos/ancho; estructuras no representables se registran para revisión, sin pérdida silenciosa. No se detectaron merges en esta pasada, pero el reparador HTML5 puede cambiar la estructura final.
- **HTML inválido y errores:** parsear con estrategia determinista HTML5, registrar avisos por ID/ruta/tipo y requerir revisión ante reparación ambigua. No registrar cuerpos, texto privado, credenciales ni valores completos de celdas. La salida debe validarse y sanitizarse nuevamente al renderizar.

## Riesgos y pendientes

- **Bloqueante para fijar conversión de tablas:** clasificación datos/layout y validación HTML5 de los cinco artículos con tags table (1080, 1641, 1667, 1669, 1670). La cuenta de 12 tags está confirmada; la interpretación semántica/geométrica no.
- **Revisión editorial necesaria:** determinar si 37 `alt=""` son decorativos o contienen información cuyo texto alternativo falta. No inventar alt ni convertir automáticamente esos vacíos en alt descriptivo.
- **Contrato RichText:** h5 en dos artículos y blockquote en uno necesitan decisión de preservación semántica antes de transformar esos artículos. Enlaces con href seguros todavía deben validarse por URL destino.
- **Responsive:** dimensiones `width` y clases de alineación deben eliminar dependencia rígida en el frontend nuevo; las capturas previas ya documentan overflow en ejemplos, pero no se reejecutó Playwright en esta fase.
- **Cobertura:** esta consulta cubrió solo `blog_body`. No audita imagen de portada `blog_images`, archivos adjuntos, scripts externos ni el HTML generado final. Tampoco verifica la intención editorial de los valores.
- **Estado editorial:** los 42 artículos siguen `import_authorized=No`. La estructura pública confirmada es evidencia para diseño, no aprobación de importación/publicación.

## Fuentes

- `docs/21_MANIFIESTO_CONTENIDO_VIGENTE.csv` (42 IDs/rutas A con template `blog-post`).
- Restauración local de ProcessWire: tabla `field_blog_body`; consulta SELECT acotada al manifiesto con `pw_auditor`.
- `docs/gbitcorp.com/site/templates/blog-post.php` (renderizado del cuerpo legado; solo lectura).
- `docs/12_PROBLEMAS_RESPONSIVE.md` (overflow móvil de imágenes/tablas).
- `docs/20_VALIDACION_CODIFICACION.md` (latin1/CP1252, UTF-8 de sesión, entidades).
- `editorial/models.py` y `editorial/blocks.py` (contrato implementado actual).
- Capturas/texto preservados en `docs/reference/blog/posts/` para cotejo visual; no se modifica ni reinterpreta su contenido en esta fase.
