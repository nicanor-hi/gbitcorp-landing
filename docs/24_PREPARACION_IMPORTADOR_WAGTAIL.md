# 24 — Preparación del importador Wagtail (diseño, no implementado)

No se creó código de aplicación/importador ni migraciones Django. La cuenta local `pw_auditor@127.0.0.1` fue confirmada en MySQL portable `8.4.4` con `USAGE ON *.*` y `SELECT, SHOW VIEW` exclusivamente en `processwire_gbitcorp_local`. El análisis usó la allowlist de 49 rutas y evitó consultas a valores sensibles. No se usó root ni producción. El grant permite técnicamente leer todas las tablas del esquema, por lo que el control de alcance de consultas sigue siendo obligatorio.

La auditoría confirmó las 49 relaciones ruta→ID→jerarquía→template. Se identificaron 10 repetidores de Home, 19 bloques de contenido y 64 herramientas en cuatro páginas de servicio, cinco categorías vinculadas y mostradas, 75 referencias `blog_images` A (74 de artículos y una del índice), 83 iconos y 14 imágenes de servicio, todas con archivo local. La imagen del índice `site/assets/files/1037/1144-1.jpg` se usa como fondo del encabezado. `blog_tags` apunta a 191 destinos únicos y no se observó uso en los templates públicos revisados; queda excluido. El título DB de ID 1086 coincide con el título público al normalizar espacios y retirar marca; el encabezado visible procede de `blog_body` y la salida H4 de `$page->title` está comentada. EULA se renderiza desde HTML estático.

La metadata confirma `latin1` en columnas de contenido, mientras la sesión MySQL usa `utf8mb4`; CP1252 de bytes almacenados coincide con la conversión UTF-8 de MySQL para 49 títulos, 42 resúmenes y 42 cuerpos. No se detectaron marcadores comunes de mojibake ni U+FFFD. Hay signos `?` literales en 8 cuerpos y 7 resúmenes; no corregirlos automáticamente, pues aparecen en el contenido preservado y la intención original de cada signo no puede inferirse. El cotejo visual/textual fue muy alto pero no exacto para todos los resúmenes/cuerpos; revisar esos contenidos editorialmente antes de publicar.

## Contrato del proceso futuro

1. Leer `21_MANIFIESTO_CONTENIDO_VIGENTE.csv` como allowlist cerrada. Rechazar páginas/plantillas/rutas que no estén en el manifiesto, incluso si el status de ProcessWire indica On.
2. Revalidar ruta→ID→template contra la cuenta RO, registrar `CURRENT_USER`, versión/puerto/base y abortar ante origen distinto a loopback local.
3. Resolver solo dependencias B referenciadas por páginas A. Incluir `pages` auxiliares únicamente cuando sea necesario reconstruir sección visible; no asignarles URL ni publicar como página Wagtail por defecto.
4. Respetar el charset `latin1`/CP1252 confirmado y convertir en memoria a UTF-8 una sola vez. No reinterpretar como ISO-8859-1, no corregir signos `?` con heurísticas ni mutar el origen. Detener registros con charset ambiguo.
5. Generar `dry-run` con relaciones, fields, assets y discrepancias. No exportar campos privados a logs. Exigir aprobación de contenido/modelo y copia de seguridad del destino antes de cualquier escritura.
6. Crear/upsert idempotente por clave de origen interna (ID + ruta), nunca duplicar; mapear IDs viejos a nuevos; conservar rutas/jerarquía; producir redirects solo cuando sean aprobados.
7. Importar solo assets B; verificar existencia, MIME, dimensiones y hash; asignar alt/caption revisados; renditions adaptables Wagtail; omitir cachés, logs, backups, sesiones/configuración.
8. Crear contenido como borrador y conciliar visualmente contra `reference/**/page.json`, `content.txt` y capturas antes de publicar. Históricos C y sensibles D quedan denegados por defecto.

## Mapeo de tipos y errores

| ProcessWire | Tratamiento importador |
|---|---|
| `pages` raíz pública | Page model Wagtail por template observado; garantizar path y padre |
| `FieldtypeRepeater` | StreamField blocks/child structure B con orden; no crear public URLs |
| `FieldtypePage` | relación explícita mediante map old-id→new-id, solo targets permitidos |
| Textarea/HTML | decode de entidades una vez, sanitización allowlist, revisión editorial y prueba UTF-8 |
| Image/File | localizar bajo `site/assets/files/<page-id>/`, cotejar con asset manifest y uso A |
| Estado, admin, usuarios, comentarios, forms submissions | D o C; excluidos por defecto. Nunca copiar auth/hash/session/config |
| Plantilla no asignada a A | excluida salvo cambio de alcance aprobado |

Errores de ruta duplicada, referencia sin target, archivo ausente, contenido con encoding ambiguo o charset inválido deben detener esa fila/lote, quedar en un reporte redactado y no convertirla silenciosamente. El proceso completo debe ser reanudable/idempotente y no borrar/reescribir ediciones hechas en Wagtail.

## Pendientes antes de implementación

- Revisión editorial de los cuerpos/resúmenes con signos `?` literales y de los textos cuya comparación con capturas no fue exacta; no intentar reconstruir automáticamente caracteres supuestamente perdidos.
- Revisión MIME, hash, dimensiones, alt, licencia y orden de assets; clasificación contextual de los 13 URL/tipo sin ruta local.
- Aprobación editorial de las 49 rutas y sus dependencias B; no se incluye contenido C ni D ni contenido adicional sin autorización.
- Definición/modelos/bloques StreamField y estrategia de PostgreSQL/UTF-8 en la fase de implementación aprobada.
