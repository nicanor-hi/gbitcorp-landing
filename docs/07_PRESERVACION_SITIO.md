# 07 — Preservación del sitio público

## Método

Se inspeccionó primero `AGENTS.md`, `CONTEXT.md` y el documento local de Playwright. El rastreo utilizó exclusivamente Playwright 1.61.1/Chromium 1228 instalados por Volta. Se inició desde `https://gbitcorp.com/`, siguió recursivamente enlaces del HTML, incluyó dos rutas estáticas halladas en templates ProcessWire y consultó `robots.txt` y `sitemap.xml`.

El rastreo elimina fragmentos para evitar ciclos y limita el dominio navegable a `gbitcorp.com` y `www.gbitcorp.com`. Cada salto de redirección se preinspeccionó sin seguir automáticamente una salida externa. Los enlaces externos se registraron sin abrir sus destinos; enlaces especiales se registraron sin activarlos. No se ingresó ni envió información en formularios.

## Cobertura verificada

- 51 destinos internos únicos intentados: 49 páginas HTTP 200 y 2 errores previos a navegación por certificado de `www.gbitcorp.com`.
- 1,645 apariciones de enlaces en las 49 páginas capturadas: 992 internos, 414 externos y 239 especiales; 0 destinos no resueltos en el DOM.
- `robots.txt` y `sitemap.xml` respondieron HTTP 404. No se encontró paginación adicional accesible desde el listado de blog durante este recorrido.
- Las URLs externas no se visitaron como páginas. Algunas imágenes/scripts referenciados por el propio HTML se cargaron durante el render del sitio; sus referencias de recursos externos se guardaron sin query strings.
- Las rutas, títulos, resultados y errores están en [08_INVENTARIO_COMPLETO_URLS.md](08_INVENTARIO_COMPLETO_URLS.md), [reference/manifest.json](reference/manifest.json) y [reference/links.csv](reference/links.csv).

## Capturas y contenido conservado

Se guardaron **351 PNG válidos** (aprox. 396 MB): 49 capturas completas en cada una de las siete resoluciones —1920×1080, 1440×900, 1366×768, 1024×768, 768×1024, 390×844 y 375×812—; cinco estados móviles de menú; dos estados de avance de carrusel; y una captura de foco de campo del formulario. El manifiesto confirma tamaño/firma PNG y registra ruta por archivo.

Cada carpeta de ruta bajo `docs/reference/` contiene:

- `content.txt`: texto visible completo extraído del DOM.
- `page.json`: título, URL final/estado, metadatos, encabezados, orden de secciones, texto de cada sección, imágenes, fondos, botones, formularios y enlaces.
- `page.md`: ficha humana con relaciones a capturas y texto.
- Capturas PNG identificadas por viewport; algunos controles interactivos tienen capturas adicionales.

`responsive.json`/`responsive.csv` guardan scroll width, client width y elementos fuera del viewport para cada página y tamaño. `assets.csv` relaciona recursos vistos con rutas coincidentes en el respaldo local. Se mapearon 933 apariciones de imágenes/fondos, 239 recursos únicos; 226 tienen archivo coincidente en el respaldo. El respaldo original no se copió ni modificó.

## Límites pendientes

- No se pueden descubrir páginas huérfanas, privadas o no enlazadas sin la base MySQL ni acceso al administrador.
- Las dos rutas `www` fallaron por `ERR_CERT_COMMON_NAME_INVALID`; las rutas equivalentes sin `www` respondieron, pero la variante exacta queda registrada como inaccesible.
- La página se preservó en el estado público de esta sesión. Variaciones de contenido en carruseles autoplay, datos personalizados o cambios posteriores del sitio no están cubiertos por una única captura.
- Para mantener la restricción sobre el respaldo, los assets originales quedan referenciados por ruta relativa dentro de `docs/gbitcorp.com/`; no se duplicaron en `docs/reference/`. Si se retira ese respaldo local, habrá que autorizar una selección de copias de assets para que la referencia sea autosuficiente.
- No se probó envío de formulario, CRM, chat, redes sociales, links externos ni operaciones que generen datos.

La segunda inspección específica del Home (carga, recursos, fondos y evidencia inicial/post-carga en desktop/tablet/móvil) está en [14_DIAGNOSTICO_HOME_RENDIMIENTO.md](14_DIAGNOSTICO_HOME_RENDIMIENTO.md). Sus capturas se añadieron a `reference/home/`; sus medidas puntuales complementan, no reemplazan, las capturas de los siete viewports de preservación.
