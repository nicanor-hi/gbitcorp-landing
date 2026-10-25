# 06 — Plan de migración por fases

## Fase 0 — Auditoría y preparación (esta fase)

- Proteger respaldo ProcessWire y documento Playwright con reglas específicas `.gitignore`; confirmar que ninguno está rastreado.
- Crear `.venv/` aislado sin instalar dependencias del producto.
- Auditar el respaldo en lectura y recorrer las rutas públicas alcanzables; registrar URLs, enlaces y responsive.
- Entregar arquitectura propuesta, limitaciones y riesgos. Detenerse para aprobación antes de implementar.

## Fase 1 — Cierre de alcance y decisiones

- Acordar páginas que se conservarán, contenido del blog, EULA, vacantes, servicios y formulario Zoho.
- Resolver certificado/canonical de `www`, rutas externas/subdominios y URLs huérfanas.
- Elegir y documentar parches Python/Django/Wagtail/PostgreSQL; actualizar Python 3.10.5 local a un parche soportado antes de instalar.
- Determinar fuente de contenido: curación manual o export MySQL autorizado. Definir aceptación editorial y responsable de aprobar textos.

## Fase 2 — Diseño de contenido Wagtail

- Convertir tipos de ruta en modelos de página y estructura padre/hijo.
- Definir bloques StreamField, snippets/settings, SEO, permisos de edición e imágenes/documentos.
- Mapear URL antigua a URL nueva; precisar redirecciones 301 y canonicals.
- Definir contrato de formularios, consentimiento, protección antiabuso, destino Zoho y manejo de errores.
- Aprobar diseño de bloques y reglas de navegación antes de codificar.

## Fase 3 — Implementación

- Crear proyecto Django/Wagtail/PostgreSQL, migraciones nuevas y entorno reproducible.
- Construir modelos, bloques, plantillas y navegación siguiendo patrones del proyecto.
- Migrar assets seleccionados con trazabilidad, derechos/atribución y alt text.
- Cargar contenido público revisado y configurar redirects/SEO.
- Implementar únicamente integraciones confirmadas mediante secretos externos al repositorio.

## Fase 4 — Verificación

- Comparar rutas y secciones con referencia en desktop/tablet/móvil; validar scroll horizontal, imágenes, tipografía, separadores, accesibilidad y reducción de movimiento.
- Verificar todos los enlaces internos y redirecciones; preservar enlaces externos y acciones especiales.
- Probar formularios en modo seguro sin enviar registros reales; usar destino sandbox si está disponible.
- Validar SEO, sitemap, canonical, 404, permisos de Wagtail y ciclo de edición/publicación.
- Documentar cualquier contenido inaccesible por falta de MySQL sin sustituirlo por texto inventado.

## Fase 5 — Preparación y despliegue (solo con autorización)

- Definir hosting, PostgreSQL, copias de seguridad, almacenamiento de media, HTTPS, secretos, observabilidad y rollback.
- Ensayar despliegue y restauración; fijar ventana y criterios de corte.
- No realizar cambios de DNS ni publicación hasta aprobación expresa.

## Bloqueos/riesgos vigentes

- Sin MySQL no se recuperan páginas no visibles, jerarquías completas, archivos huérfanos, historial, usuarios ni registros de formularios.
- Dos destinos `www` arrojan error de certificado en navegación actual.
- Python 3.10.5 es compatible por línea menor con Wagtail actual documentado, pero es un parche antiguo; debe actualizarse antes de dependencia/producción.
- Integración Zoho, captcha, SMTP, newsletter, EULA, mapas y vacantes necesitan confirmación de vigencia y requisitos.
- Inventario público basado en enlaces alcanzables, no prueba ausencia de rutas huérfanas.
