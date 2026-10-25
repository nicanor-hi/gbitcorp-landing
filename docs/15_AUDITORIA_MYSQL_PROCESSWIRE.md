# 15 — Auditoría local de MySQL / ProcessWire

## Alcance y método

Auditoría de solo lectura de la copia ya restaurada `processwire_gbitcorp_local`, conectada exclusivamente a `127.0.0.1:3307` en la instancia MySQL portable. Se verificó el PID del `mysqld.exe` y el puerto antes de consultar. La identidad de sesión confirmó MySQL **8.4.4**, base local seleccionada y cuenta autenticada local. No se ejecutó dump ni restauración, no se conectó a RDS y no se cambió ningún dato, tabla, usuario o configuración. El cliente recibió la contraseña por un archivo de opciones temporal con ACL limitado al usuario actual; se eliminó al terminar.

Las consultas cubrieron metadatos de `INFORMATION_SCHEMA`, conteos exactos, definiciones de campos, asignaciones template/fieldgroup, estados sin títulos ni valores de páginas, coincidencias de rutas públicas y referencias de archivos seleccionadas. Se ajustó `group_concat_max_len` solo en la sesión cliente para el conteo dinámico; ese ajuste terminó al cerrar la conexión y no alteró datos/configuración persistentes. No se leyeron filas de usuarios, passwords, sesiones, comentarios, mensajes de formularios ni valores de configuración de módulos.

## Hallazgos confirmados

- El dump declara como servidor fuente **MariaDB 10.11.16** (`5.5.5-10.11.16-MariaDB-log` en su encabezado). La copia analizada opera en MySQL 8.4.4; se deben probar compatibilidades y collation antes de cualquier importación futura.
- La base contiene **80 tablas**, todas InnoDB; las tablas usan `latin1_swedish_ci`, aunque el default de la base es `utf8mb4_0900_ai_ci`. No hay claves foráneas declaradas. La ausencia de FK no implica ausencia de relaciones: ProcessWire enlaza entidades mediante IDs, nombres de campo, `parent_id`, páginas y tablas de relación.
- Tablas base: `pages` 762 filas; `templates` 53; `fields` 67; `fieldgroups` 56; `fieldgroups_fields` 174; `modules` 108; `pages_access` 572; `pages_parents` 174; `pages_sortfields` 1; `caches` 114; `sessions` 717; `session_login_throttle` 1.
- Hay **68 tablas** `field_*`. El esquema y conteos observados están resumidos en [16 — Modelo de datos](16_MODELO_DATOS_PROCESSWIRE.md).
- Las banderas de páginas se superponen: 762 páginas registradas; 758 con `statusOn`, 21 con hidden, 46 con unpublished, 111 en trash y 82 system. No sumar estos indicadores como categorías excluyentes.
- Las 49 rutas públicas únicas con HTTP 200 preservadas tienen coincidencia exacta de path en el árbol de ProcessWire: Home 1, índice del blog 1, artículos 42, servicios públicos 4 y EULA 1. Véase [18 — Comparación](18_COMPARACION_BD_SITIO_PUBLICO.md).
- Para recursos directamente referenciados por las 49 páginas y las relaciones de carrusel del Home, se verificaron en disco 75 imágenes de artículos y 14 valores del campo `image`; ambos grupos estaban presentes. No se verificó individualmente la totalidad de 728 archivos.
- El Home (page ID 1) tiene campos configurados para título/SEO, banner, carruseles de servicios y equipo, descripción de equipo, datos de contacto y redes. Solo se consultó existencia/longitud de algunos campos y las cardinalidades de repeaters, no texto privado ni datos de contacto.

## Riesgos y límites

- La consulta fue autenticada como `root`, no con una cuenta SQL de solo lectura. Aunque todas las sentencias ejecutadas fueron consultas/lecturas, una siguiente sesión de auditoría debería utilizar un usuario local limitado a `SELECT` y `SHOW VIEW`, creado con aprobación y después de revisar el impacto; no se creó ahora para respetar el alcance sin escrituras.
- Las tablas tienen collation latin1 frente a default utf8mb4. Una visualización de terminal anterior mostró caracteres con mojibake; eso no prueba corrupción del contenido. Antes de importar, validar bytes/caracteres en muestras públicas concretas y planificar conversión explícita.
- El dump contiene estructuras sensibles (usuarios/password, sesiones, comentarios y mensajes de formulario). Se excluyeron sus valores y no se copiarán al nuevo CMS.
- Las consultas de rutas comprobaron 49 matches, no que cada una de las otras 713 filas represente una página publicable. El universo incluye contenido de sistema, repetidores, administración, papelera, oculto e histórico.
- No se hizo una exportación completa de contenido, ni una lectura de todos los campos o archivos; la correspondencia detallada de medios se completará solo en el alcance público y tras proteger datos.

## Fuentes y clasificación

**Hechos:** servidor/puerto/base autenticados localmente, esquema y conteos SQL, ruta coincidente y archivo existente según las consultas descritas; versión ProcessWire 3.0.229 según core local. **Inferencias:** interpretación editorial de fieldtypes/templates y propuestas Wagtail en documentos 16–19. **Pendientes:** conversión de charset, revisión del texto público campo por campo, clasificación aprobada de páginas adicionales y validación de funcionalidades históricas.
