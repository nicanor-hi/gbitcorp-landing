# 03 — Mapa de rutas y enlaces

## Método y cobertura

El inventario inicial de esta fase fue ampliado por la preservación completa en `docs/07_PRESERVACION_SITIO.md` y `docs/08_INVENTARIO_COMPLETO_URLS.md`. El rastreo final Playwright alcanzó 51 destinos internos (49 respondieron y 2 intentos a `www` fallaron por certificado) y 1,645 apariciones de enlaces. `robots.txt` y `sitemap.xml` devolvieron HTTP 404.

El inventario final conserva página de origen, elemento/texto, href original, destino resuelto, clasificación y estado de navegación en [03_INVENTARIO_ENLACES.csv](03_INVENTARIO_ENLACES.csv), copia del registro completo [reference/links.csv](reference/links.csv). Las 49 rutas, título, H1, descripción y canonical iniciales están en [03_INVENTARIO_RUTAS.csv](03_INVENTARIO_RUTAS.csv); el manifiesto ampliado está en [reference/manifest.json](reference/manifest.json).

## Resumen de enlaces encontrados

| Clasificación | Registros |
|---|---:|
| Interno (`gbitcorp.com` o `www.gbitcorp.com`) | 992 |
| Externo (otro hostname, incluidos subdominios distintos de `www`) | 414 |
| Especial (fragmentos, correo, teléfono, descargas u otros esquemas) | 239 |
| No resuelto | 0 |
| Total de apariciones | 1,645 |

Las cifras son apariciones, no enlaces únicos. Enlaces a subdominios de `gbitcorp.com` que no sean `www` quedan como externos según la regla de alcance; revisar en el CSV antes de decidir su migración. Los destinos externos no se rastrearon recursivamente.

## Rutas públicas

Las 49 rutas exactas, títulos y resultados HTTP se encuentran en el CSV asociado. El inventario incluye portada, cuatro páginas de negocio/servicios, listado y artículos del blog y una ruta EULA. No se infirieron páginas que no aparecieran en los enlaces examinados.

## No resueltos y errores

- Dos enlaces internos apuntan a host `www.gbitcorp.com` y fallaron con `net::ERR_CERT_COMMON_NAME_INVALID` al navegar. Mantener registrada la URL original y decidir normalización/redirección después de verificar certificado y canonical.
- Robots y sitemap no se pudieron recuperar en la comprobación complementaria; no se consideran fuentes cubiertas.
- Los enlaces especiales no se activaron si podían enviar datos, abrir sistemas externos o descargar contenido. No se enviaron formularios.
- El rastreo es finito y basado en enlaces renderizados. No demuestra que no existan rutas huérfanas o privadas.

## Clasificación usada

- **Interno:** URL relativa o HTTP(S) cuyo hostname es exactamente `gbitcorp.com` o `www.gbitcorp.com`.
- **Externo:** HTTP(S) de cualquier otro hostname, incluidos otros subdominios.
- **Especial:** `mailto:`, `tel:`, fragmento, descarga, `javascript:` u otros esquemas/acciones.
- **No resuelto:** href vacío o inválido sin destino determinable.

Antes de lanzar el nuevo sitio, comprobar cada ruta objetivo, conservar slugs cuando corresponda y crear redirecciones explícitas para cambios aprobados.
