# 25 — Cierre de auditoría ProcessWire (Fases 0–0.6.1)

## Resumen

La preservación pública se mantiene como fuente de alcance: **49 rutas A** con 351 capturas. El respaldo local declara ProcessWire 3.0.229; el dump MariaDB 10.11.16 se analiza únicamente en la copia local MySQL 8.4.4. La auditoría anterior documentó 80 tablas, 762 páginas, 53 templates, 67 fields y 728 archivos en `site/assets/files/`. La cuenta `pw_auditor` tiene lectura limitada a la base local; no se usó `root` ni se contactó AWS RDS. No se modificó la base ni el respaldo original y no se creó código Django/Wagtail.

La allowlist `21_MANIFIESTO_CONTENIDO_VIGENTE.csv` conserva 49 rutas únicas/49 IDs únicos y `import_authorized=No` en todas. La base sirve para confirmar dependencias; no amplía el alcance a páginas históricas, las 762 páginas completas ni los 728 archivos.

## A — Título de ProcessWire 1086

- **Ruta/ID/template:** `/blog/posts/green-it-piensa-verde/`, ID `1086`, `blog-post`; padre 1037 (`/blog/posts/`).
- **Título DB:** `Green IT ¡Piensa verde!  La Importancia del Reciclaje` (espacio doble antes de “La”).
- **Título de documento preservado:** `Green IT ¡Piensa verde! La Importancia del Reciclaje - Global Business IT`.
- **Encabezado visible:** el H2 capturado es `Green IT ¡Piensa verde! La Importancia del Reciclaje`; procede del HTML de `blog_body`. En `blog-post.php`, el H4 que habría impreso `$page->title` está comentado.
- La comparación read-only de la fase 0.6.1 confirma coincidencia al normalizar espacios y retirar el sufijo de marca. La plantilla base añade el título DB y sufijo al elemento HTML `<title>`, pero la captura del navegador tiene un solo espacio. No se atribuye la diferencia a una transformación concreta que no esté probada.
- **Valor para Wagtail:** conservar el encabezado y el título de documento del sitio preservado como referencias editoriales separadas; no trasladar el espacio doble. Confianza alta en la equivalencia textual normalizada; no se modificó ProcessWire ni MySQL.

## B — Conciliación de `blog_images`

| Alcance | Filas | Resultado |
|---|---:|---|
| 42 páginas públicas `blog-post` | 74 | 74 pares página/archivo; sin duplicados de par |
| Página pública `/blog/posts/` (ID 1037, `blog-posts`) | 1 | `1144-1.jpg`, archivo presente en `site/assets/files/1037/` |
| Total en manifiesto A | 75 | 75 pares y 75 nombres de archivo únicos; 75/75 locales |
| Tabla `field_blog_images` completa | 76 | Una fila queda fuera del manifiesto A y no se inspeccionó ni se incorpora |

El código `blog-posts.php` usa `$page->blog_images->first->url` como imagen de fondo del encabezado, por lo que la referencia de ID 1037 es una dependencia pública B confirmada. La diferencia anterior 75/74 se explica por contar el índice además de las 42 páginas de artículo; el total global 76 añade una fila fuera del alcance A. El manifiesto refleja 75 `blog_images` en A; no se agregaron páginas históricas.

## C — Codificación y cotejo público

Las columnas `data` examinadas (`field_title`, `field_resume`, `field_blog_body`) son `latin1`/`latin1_swedish_ci`; la sesión MySQL usó `utf8mb4` para cliente, conexión y resultados. Para todas las filas consultadas, los bytes interpretados como CP1252 coinciden con la conversión UTF-8 de MySQL: 49/49 títulos, 42/42 resúmenes y 42/42 cuerpos.

No se detectaron marcadores comunes de mojibake ni U+FFFD. Los signos `?` entre letras son bytes `0x3F` presentes en los datos, no artefactos de la conversión: aparecen en 8 cuerpos (778 ocurrencias) y 7 resúmenes (32). El cuerpo de 1086 coincide exactamente con el texto público una vez extraídas etiquetas HTML, decodificadas entidades y normalizados espacios. Para cuerpos, el cotejo obtuvo contención exacta en 29/42 y mediana de 99,9% de cobertura de shingles de ocho palabras. Para resúmenes comparados contra el índice, hubo 0/42 contenciones exactas y mediana de 94,1% de cobertura; las siete filas con `?` quedaron entre 94,7% y 95,5%. Los shingles son indicio de correspondencia textual, **no** prueba de identidad íntegra.

Conclusión: el problema detectado no proviene de interpretar latin1 como ISO-8859-1; el transporte CP1252→UTF-8 queda verificado para las muestras. Los signos `?` ya están almacenados. En los cuerpos con contención exacta —incluido 1086— la referencia pública conserva este patrón; no se verificó posición por posición para todos los resúmenes. No puede inferirse qué caracteres se pretendían antes de almacenarlos. Mantener la referencia pública y no reparar por heurística. La comparación exacta de todos los resúmenes/cuerpos no está demostrada; revisar contenido afectado antes de importarlo o publicarlo.

## D — Dependencias, exclusiones y preparación

- Medios confirmados A/B: 75 `blog_images`, 83 `icon` y 14 `image` (172 referencias, todos los archivos existentes). Los otros recursos se rigen por `23_INVENTARIO_ASSETS_VIGENTES.md`; no copiar los 728 archivos completos.
- Se mantienen excluidos los 191 destinos de tags sin uso público confirmado, nueve páginas adicionales `service_service`, registros históricos no preservados y contenido administrativo/sensible.
- El futuro importador debe leer exclusivamente el CSV como allowlist aprobada, mapear IDs y relaciones, convertir CP1252 a UTF-8 una sola vez, crear borradores, validar assets y reportar discrepancias sin datos sensibles. No publicar automáticamente.
- No se aprobaron importaciones; formularios/Zoho, licencias de assets, el cotejo editorial de `?` y resúmenes no exactos requieren decisiones separadas.

## Estado y recomendación

**FASE 0.6.1 completada con limitaciones no bloqueantes para iniciar FASE 1 técnica.** No hay bloqueo de codificación de transporte ni de conciliación de `blog_images`. La revisión manual de los textos con `?` y del cotejo no exacto sí es requisito antes de importar/publicar esos contenidos; conservarlos como borradores o pendientes editoriales y no “corregirlos” automáticamente.

Se recomienda iniciar FASE 1 solo con autorización expresa: seleccionar versiones compatibles, crear la estructura Django/Wagtail y definir modelos/StreamField a partir de las 49 rutas preservadas. Mantener el importador fuera del alcance hasta aprobar el modelo y resolver el flujo de revisión editorial. No se ejecutaron commits ni pushes.
