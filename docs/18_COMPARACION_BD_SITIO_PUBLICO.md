# 18 — Comparación entre base local y sitio preservado

## Método

Se tomaron las URLs únicas HTTP 200 de `docs/03_INVENTARIO_RUTAS.csv` (también listadas en `docs/08_INVENTARIO_COMPLETO_URLS.md`). Para cada una se comparó su path con la ruta calculada desde `pages.parent_id` y `pages.name` en ProcessWire. La consulta se restringió a esos 49 paths y solo devolvió ruta, ID, nombre de template y status; no incluyó título, cuerpo ni valores privados.

## Resultado de coincidencia

| Familia/ruta preservada | Rutas públicas | Match DB exacto | Template / evidencia |
|---|---:|---:|---|
| `/` | 1 | 1 | `home`, status 9 |
| `/blog/posts/` | 1 | 1 | `blog-posts`, status 1 |
| `/blog/posts/<slug>/` | 42 | 42 | `blog-post`, status 1 |
| `/negocio/.../` | 4 | 4 | `service_service`, status 1 |
| `/eula/quickbook/` | 1 | 1 | `eula`, status 1 |
| **Total** | **49** | **49** | todos los paths HTTP 200 consultados coinciden |

La cobertura exacta de ruta es 49/49; no significa que el contenido almacenado sea idéntico byte a byte al DOM preservado. La documentación pública textual completa está en `docs/reference/**/content.txt` y estructura/metadatos en `page.json`/`page.md`.

## Páginas adicionales y estados

La base tiene 762 registros `pages`, incluyendo administración, páginas de sistema, repetidores, taxonomy, trash y contenido oculto/no publicado; no se deben presentar como 762 páginas públicas. Por template/status hay 13 páginas `service_service` status 1 y solo cuatro coinciden con las páginas de servicio rastreadas. Los nueve registros adicionales de esa plantilla con status On son **C — no confirmados** y quedan excluidos; este informe no divulga sus títulos ni rutas. Solo evidencia pública nueva y aprobación explícita podrían cambiar su clasificación.

También existen familias de taxonomy/soporte de blog, clientes, productos, portfolio y casos de éxito, así como filas con flags hidden, unpublished o trash. Se registraron 199 filas `blog-tag` status On y 5 `blog-category` status On (más 1 categoría en trash); no se promueven a A ni a páginas independientes por status/conteo. Los artículos status On totalizan 42 y coinciden con las 42 URLs documentadas; hay filas adicionales de artículos en trash/no publicadas. La allowlist A se limita a las rutas públicas preservadas; dependencias B solo se determinan por uso visible.

## Recursos asociados

- Bajo `site/assets/files/` hay 728 archivos en el respaldo original.
- El cruce directo verificó que 75 referencias de `blog_images` para las 42 páginas de artículo encontraban archivo local y 14 referencias de `image` en el conjunto consultado también encontraban archivo. Las filas de archivos con descripción, metadata y nombres personales no se copiaron al informe.
- El inventario visual público identifica 933 apariciones y 239 recursos únicos (226 con coincidencia local), según `docs/10_RECURSOS_VISUALES.md`. Son métricas de recursos de páginas públicas, no un censo de las 728 entradas de `assets/files`.
- No se verificó exhaustivamente cada archivo, directorio, focal point, alt text o relación para las 49 páginas. Confirmar IDs y nombres en una etapa de importación curada.

## Diferencias y limitaciones

El SQL fue consultado bajo collation de tablas `latin1_swedish_ci`; el terminal mostró mojibake en pruebas previas. No se comparó el texto de SQL con el DOM para evitar divulgar datos y hasta resolver la codificación. La base puede conservar estado histórico que ya no está en el sitio. Asimismo, URLs `www` fallidas por certificado no se incluyeron entre las 49 HTTP 200, y deben seguir tratándose según el mapa de enlaces existente.

**Hechos:** 49/49 rutas exactas, templates/status para esas rutas, conteos de filas y archivos especificados. **Inferencia:** los nueve `service_service` extra no están respaldados por esta preservación. **Pendiente:** evaluación editorial únicamente si aparece evidencia pública adicional y cotejo de texto/medios tras resolver charset.
