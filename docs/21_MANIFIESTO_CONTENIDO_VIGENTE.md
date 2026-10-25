# 21 — Manifiesto de contenido vigente

## Regla de alcance

La evidencia del sitio público preservado determina qué URLs pertenecen al alcance inicial: **49 páginas HTTP 200**, listadas una por una en [21_MANIFIESTO_CONTENIDO_VIGENTE.csv](21_MANIFIESTO_CONTENIDO_VIGENTE.csv). La captura pública precede a la disponibilidad de la copia MySQL. La base sirve para mapear páginas/campos/dependencias, no para ampliar la allowlist por sí sola.

El CSV incluye URL/path original, clasificación A, HTTP observado, ID/template/status, un modelo Wagtail candidato, cantidad de apariciones de recursos observados y enlaces a `page.json`/`content.txt` público. El mapeo ruta→ID/template proviene de la verificación SQL previa de 49/49; FASE 0.6.1 validó que el manifiesto sigue teniendo 49 rutas/IDs únicos y reconcilió las referencias de medios sin repetir la consulta general de rutas. No contiene valores de campos privados. No es autorización para importar/publicar: `import_authorized=No` en las 49 filas hasta aprobación editorial.

## Composición verificada por fuente pública

- Home `/`: 1.
- Índice `/blog/posts/`: 1.
- Artículos públicos `/blog/posts/<slug>/`: 42.
- Páginas de negocio `/negocio/.../`: 4.
- EULA pública `/eula/quickbook/`: 1.
- **Total: 49.** Capturas/texto están organizados en `docs/reference/`; la lista extensa y estados están en [08_INVENTARIO_COMPLETO_URLS.md](08_INVENTARIO_COMPLETO_URLS.md).

## Mapas de template y contenido

La asignación ruta→ID/template se confirmó en la auditoría SQL previa. FASE 0.6.1 usó exclusivamente `pw_auditor` sobre MySQL local para las comprobaciones puntuales, sin repetir el rastreo general. Para recursos de artículos, la reconciliación confirmó 74 filas `blog_images` en las 42 páginas `blog-post` y una fila adicional en la página pública de índice (`1037`, `blog-posts`), para 75 referencias A. El resto de las 76 filas globales queda fuera del manifiesto y no se incorpora. El inventario público de recursos fuente de navegador está en `docs/reference/assets.csv`.

Las plantillas asociadas a estas rutas son `home` (1), `blog-posts` (1), `blog-post` (42), `service_service` (4) y `eula` (1). La fila `blog_images` de la página `blog-posts` (`1144-1.jpg`) alimenta el fondo del encabezado en `blog-posts.php`, existe en `site/assets/files/1037/` y es una dependencia B del índice, no una página adicional.

## Dependencias del Home

La captura muestra las secciones Inicio/hero, Líneas de negocio, Servicios, Partner Zoho, Nosotros, Nuestra esencia, Blog, Contacto y elementos globales de navegación/footer. El código `home.php` consume fields de banner, repeaters de servicios/equipo/redes, campos de texto/SEO y las publicaciones recientes; también contiene copy estructural y el formulario externo. En el CSV se registran dependencias visuales y funcionales. Para relaciones/IDs de repetidores, su composición y valores, revalidar con la cuenta RO antes del futuro importador. El análisis responsive sigue en [14](14_DIAGNOSTICO_HOME_RENDIMIENTO.md).

## Limites

- 49 rutas A no equivalen a aprobación de cada campo ni a publicación automática; las 49 filas mantienen `import_authorized=No`.
- El título DB de la página 1086 coincide con el título público normalizando espacios y retirando el sufijo de marca. El template muestra el H2 de `blog_body`; la salida H4 de `$page->title` está comentada. Usar el título/copy público preservado como referencia editorial, sin atribuir causa técnica no probada a la normalización.
- Componentes B solo se incluirán cuando una referencia A los use efectivamente; no se convierten en páginas independientes.
- Los recursos vinculados a página que no aparezcan en `assets.csv` o el DOM preservado son pendientes, no evidencia de contenido vigente.
- Ningún contenido histórico C o interno/sensible D forma parte del CSV allowlist.
