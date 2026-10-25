# 19 — Estrategia propuesta de importación a Wagtail

No se desarrolló ni ejecutó un importador. La copia ProcessWire permanece intacta; cualquier implementación futura debe ser un proceso offline controlado, nunca conectado a producción.

## Fases propuestas

1. **Congelar el alcance fuente:** trabajar sobre `processwire_gbitcorp_local` local y una copia controlada; nunca RDS. Obtener inventario estructural con un usuario SQL de solo lectura. Seleccionar allowlist inicial de las 49 URLs públicas preservadas. Rechazar por defecto páginas ocultas, unpublished, trash, protegidas, de sistema y repetidores.
2. **Resolver codificación y relaciones:** documentar collation/charset; probar lectura y round-trip de una muestra pública con acentos. Construir árbol `parent_id`, template/fieldgroup/campos, relaciones `FieldtypePage` y orden. Resolver antes de asociar nodos hijos.
3. **Manifiesto de importación:** producir reporte de páginas/rutas/plantilla/estado y media por ruta e ID, sin valores privados. Enumerar slugs destino, colisiones, campos faltantes, archivos ausentes, destinos internos y clasificación editorial. Aprobación humana antes de crear contenido.
4. **Importar medios a Wagtail:** copiar solo imágenes/documentos vinculados a páginas aprobadas, a biblioteca administrada; preservar procedencia, nombre, dimensiones, alt/caption confirmado y hash. Nunca importar `cache`, `logs`, `sessions`, backups, configuración privada o archivos no referenciados. Crear renditions adaptativas para imágenes grandes.
5. **Importar páginas en orden de árbol:** Home, páginas de servicio/estándar, índice y artículos; luego relaciones/taxonomy aprobadas. Aplicar transformadores declarativos por template y fieldtype, bloques StreamField según el contenido confirmado, sanitización HTML y normalización de rutas. Marcar drafts inicialmente; no publicar automáticamente.
6. **Conciliar y probar:** comparar número y URL, contenido visible, imágenes, metadatos SEO y relaciones contra el sitio preservado; validar links internos, responsive y snapshots. Generar reporte de discrepancias y permitir reejecución idempotente mediante clave de origen estable (ID/ruta), sin duplicar páginas ni pisar ediciones Wagtail.
7. **Publicación/corte posterior:** aprobación editorial, redirects verificados, estrategia canonical/www, backup PostgreSQL y plan reversible antes de cualquier despliegue. Fuera del alcance de esta auditoría.

## Mapeos a validar

| Fuente | Destino propuesto | Regla |
|---|---|---|
| `pages` + template y árbol | modelos Wagtail Page | preservar ruta pública y padre, usar allowlist; no importar filas por conteo global |
| `fields`/fieldgroups | campos de modelo/paneles | solo campos editoriales confirmados para templates activos |
| `FieldtypeRepeater` y páginas `repeater_*` | StreamField structurado o relación explícita | mantener orden, mapear cada tipo comprobado; no crear URLs de repeater |
| `FieldtypePage` | FK/M2M/taxonomy | resolver ID ProcessWire → ID destino y revisar targets permitidos |
| Textarea/HTML | RichText/StreamField | limpiar entidades y markup peligroso con allowlist; revisión visual |
| Image/File | Wagtail Images/Documents | localizar en `site/assets/files/<page-id>/`; solo activos referenciados por página aprobada |
| `metaDesc`, title, name | SEO title/description, slug | mantener ruta antigua exacta cuando sea viable y probar acentos/canonical |
| formularios, usuarios y sistema | excluidos | definir aparte; nunca importar submissions, passwords/sessions o configuración/secrets |

## Criterios de seguridad y calidad

- La herramienta futura debe soportar `--dry-run`, salida redactada, validación de origen local, conteo de filas/medios, límites explícitos y confirmación. Nunca aceptar un host remoto por configuración implícita.
- No leer ni transportar password, usuarios, sesiones, comentarios ni mensajes de formulario. La base contiene esos tipos de información aunque no se examinaron valores.
- Las sentencias de importación deben ir a un entorno PostgreSQL de prueba aprobado, no en la fase actual. Proteger credenciales por secret manager/variables efímeras.
- No normalizar Unicode o slash final sin comparar URLs históricas; generar redirects solo para cambios aprobados.
- Validar imágenes (mime, extensión, tamaño, dimensiones), escapes HTML y enlaces externos. Mantener origen/ID como trazabilidad de migración, no como dato visible.
- Registrar cifras y errores sin copiar cuerpo ni PII; reejecución debe evitar duplicados y nunca borrar páginas editadas.

## Pendientes de aprobación

1. Aprobar o ajustar explícitamente la allowlist de 49 rutas. Los nueve `service_service` adicionales permanecen excluidos como clase C salvo evidencia pública y autorización explícita.
2. Confirmar si blog categories/tags, EULA, portafolio/casos, productos y páginas de clientes siguen vigentes.
3. Definir cuentas/roles Wagtail, privacidad/retención de datos y destino CRM/contacto.
4. Aprobar estrategia de charset y pruebas de compatibilidad fuente MariaDB 10.11.16 → destino PostgreSQL.
5. Aprobar modelos StreamField y campos requeridos antes de implementar importador.
