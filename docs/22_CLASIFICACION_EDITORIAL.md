# 22 — Clasificación editorial

## Criterio

La presencia en MySQL no determina vigencia. La preservación pública define el alcance; las consultas locales de solo lectura solo identifican los datos auxiliares necesarios para reproducir esas páginas.

| Clase | Regla | Tratamiento |
|---|---|---|
| **A — Público confirmado** | URL HTTP 200 incluida en el rastreo y con captura/texto preservado | 49 rutas en el manifiesto. Candidatas a migración, no autorización de publicación automática. |
| **B — Dependencia del contenido público** | Asset, registro repeater, relación, categoría o componente compartido usado por una página A visible | Incluir solo como dependencia de la página A; no generar URL pública por defecto. |
| **C — Histórico o no confirmado** | Página, sección, relación o registro sin respaldo en la preservación vigente | Excluir por defecto. No promover por estado ProcessWire, template o existencia en la base. |
| **D — Interno o sensible** | Administración, usuarios/autenticación, sesiones, comentarios privados, envíos de formularios y configuración privada | Excluir del CMS público y no documentar sus valores. |

## Clasificación confirmada

- **A:** 49 URLs públicas: Home, índice de blog, 42 artículos, cuatro páginas de servicio y EULA. Las 49 tienen página ProcessWire, ruta jerárquica y template confirmados mediante consultas SQL locales de solo lectura. El título almacenado coincide con la referencia en 47 de 48 páginas cuyo template consume título de DB; el artículo ID 1086 necesita revisión. EULA se representa desde HTML estático.
- **B:** Home: 10 páginas auxiliares de repetidores (4 `carousel_services`, 3 `carousel_us`, 3 `social_med`). Cuatro páginas de servicios: 19 elementos `content` y 64 elementos `tools`; no se encontró contenido útil en `clients`. Blog: cinco categorías vinculadas mediante 40 relaciones y visibles como filtros en la preservación. Son dependencias, no páginas migrables automáticamente.
- **C:** 191 destinos únicos de `blog_tags` (381 relaciones) no aparecen en la representación vigente inspeccionada y no son consumidos por los templates públicos de artículo/listado revisados. Excluir hasta hallar evidencia pública o aprobación. También se excluyen las nueve páginas `service_service` adicionales que no están entre las rutas A. La falta de rastreo por sí sola no prueba obsolescencia absoluta.
- **D:** Hay estructuras de autenticación, sesión, comentarios y formularios/envíos. No se consultaron valores privados. Los valores de contacto del Home/footer no fueron exportados a documentación; su selección editorial debe ser explícita.

Las cifras no son aditivas: los registros B pueden ser filas técnicas de `pages` y seguir sin ser páginas públicas independientes. No se consultaron contenido privado, tags individuales ni las nueve páginas adicionales.

## Evidencia y pendientes

**Confirmado:** referencias SQL para las 49 rutas, relaciones B descritas y recursos locales cotejados (ver informes 21 y 23). **Pendiente:** aprobación editorial final, cotejo completo de textos HTML y resolución manual del título ID 1086. El manifiesto `21_MANIFIESTO_CONTENIDO_VIGENTE.csv` es una allowlist candidata; conserva `import_authorized=No`.
