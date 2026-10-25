# 05 — Propuesta de arquitectura Django/Wagtail

Esta propuesta se basa en la estructura ProcessWire y las 49 rutas públicas observadas. Es una decisión de diseño pendiente de aprobación; no se crearon modelos, aplicaciones ni migraciones.

## Modelos de página

- `HomePage`: hero, CTA, líneas de negocio, servicios, partners, equipo/clientes, esencia, artículos destacados y formulario. Composición con StreamField para permitir reordenar secciones sin una plantilla monolítica.
- `BusinessPage` o página de servicio: título, resumen, imagen, cuerpo y CTA; usar una familia de páginas solo donde las rutas y contenido reales compartan estructura.
- `BlogIndexPage` y `BlogPostPage`: listados/paginación, título, fecha, categorías/tags si son confirmados, imagen de portada, contenido StreamField, SEO y enlaces relacionados.
- `StandardPage`: contenido informativo/EULA y páginas sencillas. Confirmar vigencia y estructura de `/eula/quickbook/` antes de mantenerla.
- Evitar crear modelos para contenido inferido solo por nombres de plantillas antiguas.

## Contenido compartido y medios

- Wagtail Images y Documents para medios gestionables, con textos alternativos, captions y renditions apropiadas.
- `StreamField` con bloques acotados para hero, texto, imagen/texto, grilla de servicios, logo/partner, tarjetas y CTA. Definir bloques tras inspeccionar todas las rutas objetivo.
- Snippets o settings para navegación, redes sociales, datos de contacto y footer solo si son globales y realmente compartidos; mantener permisos de edición acotados.
- Reutilizar recursos originales seleccionados con manifiesto de ruta/procedencia; no migrar directorios de cache, sesiones, logs o archivos no asociados.

## URL, SEO y redirecciones

- Preservar slugs y jerarquía públicos donde sea posible. Mantener una tabla ruta antigua → página Wagtail para cobertura y redirecciones.
- Configurar títulos SEO, descripciones, canonical, sitemap y metadatos sociales desde contenido revisado.
- Wagtail Redirects para cambios aprobados y comprobados. Resolver los casos `www`/certificado y canonical antes del corte.
- No cambiar rutas con acentos o normalización de slugs sin revisar el inventario CSV y referencias externas.

## Formularios e integraciones

- El formulario de portada apunta actualmente a Zoho CRM; el comportamiento exacto y destino activo deben confirmarse con el propietario. No replicar credenciales ni campos ocultos del HTML antiguo sin validar procedencia.
- Implementar validación de servidor, protección antiabuso, consentimiento y transporte seguro. Definir retención mínima de datos y logging sin datos personales.
- No se debe asumir que newsletter, SMTP, captcha, Maps o el módulo SimpleContactForm siguen activos; confirmar cada caso.

## Base de datos y dependencias

- PostgreSQL nuevo para Django/Wagtail; no conectar ni migrar sin autorización a la base ProcessWire.
- Hay una copia local restaurada de ProcessWire, auditada en solo lectura; el resumen está en `15_AUDITORIA_MYSQL_PROCESSWIRE.md`. La importación pública podrá ser asistida/curada, pero no se deben trasladar páginas privadas, usuarios, envíos o configuración sensible. Charset y asociaciones completas de medios requieren validación.
- El Python local es 3.10.5. La matriz oficial de Wagtail 8.0 indica compatibilidad con Python 3.10 y Django 5.2, 6.0 o 6.1; actualizar al último parche Python vigente antes de fijar versiones y verificar compatibilidad de dependencias adicionales.

## Referencias técnicas

- [Compatibilidad Django/Python de Wagtail 8.0](https://docs.wagtail.org/en/v8.0.1/releases/upgrading.html#compatible-django-python-versions).
- [StreamField](https://docs.wagtail.org/en/stable/topics/streamfield/).
- [Modelos de página](https://docs.wagtail.org/en/stable/topics/pages/).
- [Snippets](https://docs.wagtail.org/en/stable/topics/snippets/).
