# 23 — Inventario de assets del sitio público

## Fuente e inventario

La referencia primaria es [reference/assets.csv](reference/assets.csv), generada desde recursos observados en las páginas preservadas, junto a `page.json` y capturas. El inventario registra **933 apariciones**, **239 URL/tipo únicos**, **226** con coincidencia local y **13** sin coincidencia. No clasificar los 13 como rotos automáticamente. Hay **728 archivos** totales bajo `docs/gbitcorp.com/site/assets/files/`, pero solo el subconjunto ligado a A es candidato. No se copiaron ni alteraron archivos originales.

La conciliación SQL local read-only confirma **172 referencias de medios en el alcance A**: `blog_images` 75/75, `icon` 83/83 e `image` 14/14; todas tienen archivo local. De `blog_images`, 74 filas corresponden a 42 páginas `blog-post` y una a la página de índice `1037` (`/blog/posts/`, template `blog-posts`). Esta última referencia es `1144-1.jpg`, bajo `site/assets/files/1037/`, y `blog-posts.php` la usa como imagen de fondo del encabezado; es una dependencia pública B. En total hay 75 pares página/archivo y 75 nombres de archivo únicos en A. La tabla completa contiene 76 filas: una fila no pertenece al manifiesto A y se excluye, sin inspeccionar ni incorporar su contenido. No hubo referencias pobladas de `blog_files` en las páginas A consultadas. Los 728 archivos completos no se inspeccionaron ni aprobaron.

## Categorías de uso observado

| Tipo | Evidencia y tratamiento propuesto |
|---|---|
| Recursos visuales bajo `site/templates/` | Logos, ilustraciones, iconografía, fondos y separadores visibles/cargados por las páginas. Referencias/rutas locales aparecen en `assets.csv`; el Home y las imágenes de fondos se detallan en `14_DIAGNOSTICO_HOME_RENDIMIENTO.md`. Copiar solo los recursos usados por páginas A y tras verificar licencia/tamaño. |
| Imágenes de contenido bajo `site/assets/files/<id>/` | Las 172 referencias de campos relacionadas con A y dependencias directas tienen archivo local; incluyen 75 `blog_images`, iconos de repetidores y 14 imágenes del tipo `image`. Importar solo tras confirmar uso/orden y aprobación editorial. |
| Otros archivos locales | El inventario agrupa 4 recursos locales en otras rutas; requieren inspección antes de selección. |
| Recursos sin ruta local coincidente | 13 URL/tipo únicos del CSV. Revisar si son servicios externos, URL dinámica, respuesta no persistida o archivo realmente ausente. No descargarlos ni importarlos sin confirmar su papel. |
| Recursos externos cargados por el sitio | URLs de servicios terceros, form/CRM/captcha/fuentes/etc. Son dependencias externas, no assets portables del proyecto. Confirmar privacidad, licencias y comportamiento antes de integrar. |

Los conteos por categoría son métricas de la instantánea previa. El detalle de cada URL, página donde aparece, alt, dimensiones, tipo, y ruta del respaldo se conserva en `reference/assets.csv`; no se duplica una lista incompleta aquí.

## Home y responsive

El Home incluye fuentes CSS estáticas y fondos de `site/templates/img/new/`: `Ciudad-Fondo.png` para hero; `Fondo-Blanco-Curvas-03.png` en servicios; `Fondo-Gris-2.png` en partner; `Fondo-de-Oficina-11.png` en Nosotros; `fondo-blanco6.png` en esencia; `Fondo-10.png` en Blog y `fondo-6.png` en Contacto. Para dimensiones, peso, `cover`, recorte y propuesta de sustitución por CSS/SVG, véase [14](14_DIAGNOSTICO_HOME_RENDIMIENTO.md). Fotos con valor editorial se mantienen como imagen responsiva; curvas/separadores estructurales deben desacoplarse del PNG rígido donde convenga.

## Faltantes/pendientes

- Los 13 URL/tipo sin coincidencia local se agrupan en 2 endpoints externos de Zoho, 2 URL de imágenes externas de Wix y 9 URL de `gbitcorp.com` que corresponden a rutas de página/dinámicas, no a paths directos de archivo local. No se visitaron destinos externos ni se declararon rotos; requieren inspección contextual.
- No se revisó exhaustivamente MIME, hash, dimensiones, licencia, alt ni duplicados por contenido.
- Revisar document downloads, alt, focal point, MIME real, dimensiones y duplicados por contenido antes de importarlos.
- Los recursos A/B deben quedar en un manifiesto aprobado; no copiar el directorio completo `assets/files`.
