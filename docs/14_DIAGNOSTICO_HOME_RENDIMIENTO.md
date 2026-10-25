# 14 — Diagnóstico del Home: carga e imágenes

## Alcance y evidencia

Inspección de solo lectura de `https://gbitcorp.com/` el 24-10-2026, mediante la instalación ya presente de Playwright 1.61.1 / Chromium 1228 por Volta. No se modificó ni ejecutó ProcessWire. En cada viewport se guardó una captura inicial tras `DOMContentLoaded` + 1,2 s; luego se recorrió la página para disparar carga diferida, se esperó `document.fonts.ready`, `img.decode()` y una ventana limitada de quietud de red, y se guardó la captura completa.

Viewports: desktop 1440×900, tablet 768×1024 y móvil 390×844. La evidencia incluye [móvil inicial](reference/home/audit-initial-mobile-390x844.png), [desktop completo tras carga](reference/home/audit-loaded-full-desktop-1440x900.png), [tablet completo tras carga](reference/home/audit-loaded-full-tablet-768x1024.png), [móvil completo tras carga](reference/home/audit-loaded-full-mobile-390x844.png), además de sus otras capturas iniciales y [métricas JSON](reference/home/performance-audit.json). Se inspeccionaron visualmente el estado inicial móvil y estados completos desktop y móvil; las secciones, incluidos formulario y footer, aparecen en estos últimos.

Es una medición puntual sin throttling de red configurado; los tiempos son los de esta sesión/navegador y no una garantía de experiencia para todos los usuarios. LCP no se reporta como métrica de navegación: el observador se mantuvo activo durante scroll programático y registró candidatos posteriores al scroll, por lo que no equivalen a un LCP inicial limpio. CLS medido fue 0 y no se observaron entradas de layout shift; eso no descarta cambios visuales de pintura, como el fondo de portada que tarda en aparecer. La telemetría de terceros se guardó con query strings suprimidos.

## Resultados de carga observados

| Viewport | TTFB aproximado (responseStart) | HTML recibido | DOMContentLoaded | `loadEventEnd` | Recursos en Performance | `scrollWidth` |
|---|---:|---:|---:|---:|---:|---:|
| 1440×900 | 647 ms | 649 ms | 2,414 ms | 12,770 ms | 54 | 1440 |
| 768×1024 | 612 ms | 613 ms | 3,082 ms | 17,856 ms | 54 | 768 |
| 390×844 | 622 ms | 623 ms | 2,718 ms | no terminado al snapshot (valor 0) | 52 | 405 (15 px de overflow) |

El documento HTML fue pequeño: 12.1 KB transferidos y 41.0 KB decodificados. `responseStart/End` indica que el servidor entregó pronto el HTML; la espera larga se concentra después, durante recursos externos y medios. En el navegador se registraron 8 recursos con `initiatorType=css`, 7 `link`, 10 `script`, 20–21 `img` y otros recursos. La suma de tamaños decodificados por entradas de Performance no equivale a bytes únicos transferidos: puede incluir recursos repetidos/clonados o cross-origin.

Hallazgos comprobados:

- En dos barridos los `loadEventEnd` terminados variaron entre 12,8 y 18,3 s; en el último barrido el evento seguía sin terminar al tomar la medición móvil tras la espera limitada. No se debe presentar el 0 como tiempo ni como evento exitoso. `DOMContentLoaded` se mantuvo entre 2,4 y 3,1 s.
- La captura móvil inicial, tomada 1,2 s después de `DOMContentLoaded`, muestra el fondo de ciudad solo en la parte superior y el resto del hero blanco; en la captura completa posterior sí aparece el fondo. Es evidencia de pintura visual incompleta mientras el fondo CSS aún no está disponible, no de un desplazamiento geométrico probado.
- El fondo `Ciudad-Fondo.png` pesa 5,051,028 bytes (5.05 MB). Recursos individuales del carrusel de servicios llegan a 1.47–1.92 MB; fotos del carrusel de equipo ~2.0–2.1 MB. El navegador reportó solicitudes de imagen que duraron hasta 16.9 s en estas ejecuciones.
- Las imágenes HTML observadas no declaraban `loading="lazy"` ni `srcset`; `loading` quedó en `auto`. En el snapshot inicial desktop ya se habían solicitado seis imágenes (`desplegable`, logo, servicio y dos imágenes Partner), aun cuando las de Partner estaban por debajo del pliegue; en móvil se habían iniciado cinco solicitudes y algunas imágenes distantes aún no estaban descargadas. El navegador aplica heurísticas diferentes por viewport, pero el código no expresa una política de lazy loading/tamaños adaptativos. Las dimensiones intrínsecas/atributos no reservan consistentemente las proporciones de todos los medios.
- La hoja Google Fonts solicitada (import con familias Roboto, Comic Sans MS, Times New Roman y Noto Sans) falló en Chromium con `net::ERR_BLOCKED_BY_ORB`. No se reportaron errores de consola. La fuente efectiva y el comportamiento sin acceso a ese servicio deben verificarse con navegador normal/red de producción; no se atribuye el error a un defecto definitivo del sitio.
- No se observaron respuestas HTTP 4xx/5xx en los eventos capturados. Se cancelaron solicitudes de telemetría Google al cerrar el contexto (`ERR_ABORTED`); no se consideran fallos de contenido. El widget de SalesIQ de Zoho y recursos del formulario/captcha aparecen en la carga, pero no se enviaron datos. Su peso/latencia puede variar por servicio externo.
- El segundo barrido sí registró FCP de 1.58–1.85 s. La serie LCP siguió registrando candidatos al recorrer la página (hasta 23.3 s, sección `us`), así que se descarta como LCP inicial; no se sustituye por `loadEventEnd`. CLS fue 0 en las tres mediciones; al ser una ejecución headless sin throttling no representa un CWV de campo.

### Causas comprobadas e hipótesis

**Comprobado en código y navegador:** la plantilla carga siete hojas CSS en `<head>` y un tag async de Google Analytics; Bootstrap, jQuery slim y Owl Carousel se cargan al final del body. La página incluye una importación CSS remota de fuentes. El formulario Zoho inserta scripts/recursos de terceros, incluido SalesIQ. Fondos y carruseles se cargan sin `srcset`/`sizes` ni lazy loading explícito. CSS usa fondos grandes y `background-size: cover`.

**Causa probable del `load` tardío:** la concurrencia/latencia de múltiples imágenes grandes, los dos grupos de fotografías/carruseles, fondos de secciones que ocupan mucha área, fuentes externas y servicios externos del formulario/analítica. La medición prueba la demora, pero no establece cuánto aporta cada dependencia ni prueba que scripts síncronos bloqueen el primer render. En un snapshot móvil el evento `load` seguía pendiente. No se encontró una respuesta HTTP fallida que explique por sí sola la demora.

## Secciones, imágenes de fondo y separadores

Las rutas son relativas al respaldo local ignorado por Git, bajo `docs/gbitcorp.com/`. Dimensiones/peso se leyeron de esos archivos en modo de solo lectura; las URLs corresponden a las observadas en template/CSS/red pública. Todos estos fondos se declaran inline en `home.php` con `background-repeat:no-repeat; background-position:center center`; las clases correspondientes aplican `background-size:cover`.

| Sección / intención | Archivo en ProcessWire y URL pública | Dimensiones; peso | Elemento / ajuste observado | Lectura responsive |
|---|---|---:|---|---|
| Hero, ciudad y texto de negocio | `site/templates/img/new/Ciudad-Fondo.png` · `/site/templates/img/new/Ciudad-Fondo.png` | 3126×3909; 5,051,028 B | `div.banner` con `background-image`; `cover`, centro-centro | Proporción fuente 0.80 frente a contenedor móvil ~0.37: `cover` recorta mucho ancho. En móvil el fondo no estaba pintado en la captura temprana y pesa 5.05 MB. Mantener fotografía con variantes adaptativas y foco por breakpoint; precargar/priorizar solo la variante hero adecuada. |
| Curva/divisor alrededor de servicios | `site/templates/img/new/services/Fondo-Blanco-Curvas-03.png` · `/site/templates/img/new/services/Fondo-Blanco-Curvas-03.png` | 7967×5705; 785,615 B | `section.services`; `cover`, centro-centro; alto CSS móvil observado 680 px | PNG decorativo de ~45 MP y relación 1.40 aplicado a un contenedor móvil estrecho. El recorte lateral puede cambiar la curva. Reconstruible como pseudo-elemento/CSS o SVG responsivo; conservar solo el trazo/curva, no una textura de página completa. |
| Fondo de Partner de Zoho | `site/templates/img/new/partner/Fondo-Gris-2.png` · `/site/templates/img/new/partner/Fondo-Gris-2.png` | 1913×1091; 81,243 B | `section.partner-zoho`; `cover`, centro-centro; alto móvil 780 px | Decoración de baja compresión pero proporción ~1.75 frente a ~0.50 en móvil; `cover` recorta gran parte lateral. Mantener si aporta textura, preferir CSS/SVG para la forma gris curva. |
| Foto/fondo de Nosotros | `site/templates/img/new/us/Fondo-de-Oficina-11.png` · `/site/templates/img/new/us/Fondo-de-Oficina-11.png` | 4000×2000; 2,042,392 B | `section.us`; `cover`, centro-centro; 750 px móvil | Foto 8 MP con fuerte recorte horizontal a móvil; preservar como fotografía con focal point y versión móvil, o separar foto y curva decorativa. |
| Separación en Nuestra esencia | `site/templates/img/new/customer/fondo-blanco6.png` · `/site/templates/img/new/customer/fondo-blanco6.png` | 1913×1091; 113,397 B | `section.customers#clientes`; `cover`, centro-centro; 400 px móvil | Textura/curva clara, sin contenido editorial intrínseco; candidata a SVG/CSS. |
| Fondo/divisor del blog | `site/templates/img/new/blog/Fondo-10.png` · `/site/templates/img/new/blog/Fondo-10.png` | 3600×1810; 518,971 B | `section.blog`; `cover`, centro-centro; alto CSS móvil observado 1440 px | Relación ~1.99 contra ~0.27 en móvil; el recorte central es extremo. Mantener la intención curva en SVG/CSS y hacer las cards/blog independientes y de altura natural, no fijar 1440 px por breakpoint. |
| Fondo de contacto | `site/templates/img/new/contact/fondo-6.png` · `/site/templates/img/new/contact/fondo-6.png` | 2124×1122; 394,118 B | `section.contact`; `cover`, centro-centro; alto móvil observado 1440 px | Foto/fondo ~1.89 frente a ~0.27: recorte importante y área vertical grande. Mantener la fotografía solo si tiene valor, con versión/foco móvil; evitar altura fija y ofrecer base sólida de contraste para el formulario. |

Las dimensiones de contenedor citadas proceden del DOM a esos viewports; las relaciones y magnitudes del recorte son inferencias geométricas de `cover`, no defectos visuales por sí mismos. `home.php` también contiene dos wrappers vacíos (`transition-botton overlap-1` y `transition-disabled`) sin reglas encontradas en las hojas no minificadas inspeccionadas; las curvas visibles parecen formar parte de las imágenes de fondo, pero el papel histórico de esos wrappers queda pendiente de confirmar.

Como referencia geométrica, el hero móvil de 390×1050 con una imagen de proporción 0.80 necesita escalar por alto a ~841 px de ancho; `cover` recorta aproximadamente 54% del ancho renderizado total. `services` (fondo 1.40, sección móvil ~0.57), partner (1.75 frente a ~0.50), Nosotros (2.0 frente a ~0.52), blog (1.99 frente a ~0.27) y contacto (1.89 frente a ~0.27) también fuerzan recortes horizontales pronunciados en móvil. Son cálculos de CSS/tamaño, no afirmación de que todas las curvas estén visualmente defectuosas; decidir por inspección de composición qué conservar como fotografía y qué convertir en decoración responsiva.

En tablet y móvil las capturas completas muestran un espacio vertical amplio entre las dos tarjetas del blog y la sección Contacto. DOM/CSS confirma `.blog { height: 1440px; }` también en el breakpoint móvil; el espacio excesivo es comprobado, y la altura rígida es causa directa plausible. También se observan curvas decorativas desplazadas/recortadas al cruzar entre servicios, partner y Nosotros por el solape y `cover`. Contacto mantiene 1440 px en móvil, aunque la sección termina antes del borde inferior de ese fondo en la captura, lo que debe revisarse al llevarlo a contenido de altura natural.

## Imágenes de contenido e interacciones

- Owl Carousel de servicios contiene al menos `proyectos-2.png`, `consultoria-2.png`, `outsorcing-2.png`, `capacitacion-2.png` (939×1249 cada una); ocupan 1.47–1.92 MB por archivo en el respaldo. Las opciones JS crean loop/autoplay y configuran dos elementos en móvil y cuatro en desktop; el carrusel puede clonar nodos y repetir solicitudes/decodificaciones. La lista completa aparece en el JSON de evidencia; tamaños de bytes locales se deben verificar al seleccionar qué conservar.
- Carrusel de equipo: `grupo_gbit.jpg` (~761 KB, 2822×1663), `team_ch.png` (~2.10 MB, 2823×1664) y `team_marketing.png` (~2.00 MB, 2823×1664). Dos imágenes con nodo renderizado 0×0 en un estado igualmente estaban descargadas; evidencia de bytes/DOM en JSON. Es probable que el slider/carousel precargue imágenes de otras diapositivas; confirmarlo con interacción y caché limpia.
- Imagen de fallback del blog `no-image.png`: 1296×716 y ~616 KB aunque la tarjeta se presenta pequeña. Varias imágenes de redes son cuadradas de ~3085×3085 y se muestran a 60×60: reducir rendición notablemente.
- Las imágenes visibles usan `<img src>` y algunas clases `img-fluid`; no se observó `srcset`, `sizes`, `width`/`height` HTML coherente, `fetchpriority` ni `loading=lazy`. El logo de 2373×615 se muestra a 174×45 y pesa ~51 KB.

## Reconstrucción recomendada en Wagtail

1. Maquetar como secciones HTML editables (Hero, líneas/servicios, partner, Nosotros, esencia, artículos recientes, contacto); preservar texto real, tarjetas, formulario y navegación. Separar estructura, fotografía y decoración para que el recorte no condicione el layout.
2. Para hero/fotos de valor, usar imagen Wagtail con renditions según anchos de destino, `srcset`/`sizes`, `width`/`height` o `aspect-ratio` y foco editable. Servir WebP/AVIF cuando el stack de publicación/cliente lo soporte con fallback. Priorizar una sola imagen hero que realmente se pinta al inicio; no precargar todos los fondos y carruseles.
3. Para secciones fuera de pantalla, cargar con `loading="lazy"`/renditions diferidas; reservar espacio. Carruseles deben diferir diapositivas fuera de pantalla y evitar clones/decodificación de la galería completa en móvil; evaluar si una fila de cards responsivas ofrece una solución más simple y accesible.
4. Sustituir curvas decorativas de los fondos `Fondo-*` por SVG responsive o CSS pseudo-elementos si su inspección visual confirma que solo son decoración. Mantener fotografía de ciudad, equipo y oficina optimizada con arte-dirección móvil, no estirarla como divisor.
5. Tratar como opcionales/diferidos chat, analítica y widgets de terceros según requisito confirmado; cargar formulario externo de forma que no retrase la pintura inicial y documentar privacidad/consentimiento. No trasladar configuraciones o identificadores embebidos del respaldo sin revisión de seguridad.
6. Mantener tarjetas/carruseles con controles accesibles, `prefers-reduced-motion`, foco visible y sin clones que produzcan `scrollWidth > clientWidth`. Validar capturas con el mismo contenido a 1440×900, 768×1024 y 390×844 y más tamaños del inventario responsive.

## Pendientes

- Repetir mediciones con cache fría/caliente, red limitada y dispositivo/navegador real; obtener LCP/CLS con observadores bien configurados y probar cancelaciones de terceros sin suponer que son fallos del sitio.
- Confirmar con negocio si SalesIQ, analítica Google, Zoho CRM/captcha y la importación de Google Fonts son requisitos actuales; revisar su privacidad e impacto antes de integrarlos.
- Revisar cada fondo a tamaño natural y archivo original para separar formas decorativas de fotografía/branding; seleccionar assets finales solo tras aprobación para copiar de la referencia local protegida.
- No se enviaron formularios ni se alteró producción o el respaldo. No se implementó Wagtail.
