# 02 — Inventario de assets

## Conteos observados

| Ubicación | Conteo / tipos principales | Uso y tratamiento |
|---|---:|---|
| `site/templates/img/` | 83 imágenes | Recursos de diseño distribuidos por `new`, `services`, `partner`, `customer`, `us`, `blog`, `lines`, `contact`, `portfolio` y `misc`. Revisar derechos, uso y duplicados antes de migrar. |
| `site/templates/` | 45 PNG, 36 JPG, 2 GIF, 3 SVG, iconos y fuentes | Recursos del tema/plantillas; varias versiones anteriores. |
| `site/assets/files/` | 728 archivos: 407 PNG, 259 JPG, 58 GIF, 3 JPEG, 1 TXT | Archivos CMS originales. Relación con páginas no recuperable sin MySQL. |
| `site/templates/css/` | 24 CSS en total | `new/`, `old/`, `default/`; inspeccionar referencias activas antes de seleccionar. |
| `site/templates/js/` | 29 JS en total | `new/`, `old/`, `vegas/`; bibliotecas de terceros y código histórico. |
| `site/templates/scripts/` | `main.js`, `blog.js` | Scripts propios aparentes, sujetos a verificación de uso. |
| Fuentes de plantilla | 11 archivos entre TTF/WOFF/WOFF2/EOT | Identificar fuentes realmente cargadas y licencia antes de conservar. |

El recuento global del respaldo es 3,786 archivos; incluye core ProcessWire, módulos, logs, cachés y recursos no necesariamente públicos. No se considera que todos sean reutilizables.

## Assets candidatos a reutilización

- Marca/logotipo y variantes de `templates/img` y recursos públicos cargados por la portada.
- Fotografías de equipo/clientes, iconos/logotipos de partners y miniaturas de servicios/blog cuando su uso y licencia estén verificados.
- Ilustraciones de secciones y recursos identificados como divisores; su intención visual puede reconstruirse con CSS/SVG responsive en vez de estirar una imagen.
- Recursos de `assets/files` solo después de mapearlos a páginas visibles. No copiar cachés, backups, sesiones o logs.

## Hallazgos y pendientes

- Hay carpetas explícitamente llamadas `old`; sus archivos no deben migrarse por defecto.
- El repositorio no contiene el catálogo MySQL que asigna títulos, alt, descripciones y relaciones a los archivos. Recuperar el mapeo manualmente desde páginas públicas o mediante export autorizado.
- Revisar licencias de fuentes, iconografía y librerías de terceros; no se presume permiso por estar en el respaldo.
- Generar hashes y un manifiesto de assets efectivamente elegidos en la fase de implementación, conservando ruta/procedencia original.
