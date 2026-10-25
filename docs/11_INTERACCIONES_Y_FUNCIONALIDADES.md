# 11 — Interacciones y funcionalidades observadas

## Navegación

- Header compartido con enlaces de inicio, líneas de negocio, servicios, Partner Zoho, nosotros, esencia, blog y contacto.
- El menú compacto móvil tiene botón `navbar-toggler`; se guardó el estado abierto en las páginas donde estaba disponible. No se siguieron enlaces desde el menú hacia dominios externos.
- Footer incluye contactos, enlaces internos de navegación y redes sociales. Las relaciones completas y los destinos están en `reference/links.csv`.

## Componentes de portada

- Hero con CTA de contacto.
- Tarjetas y CTA de líneas de negocio/diagnóstico.
- Carrusel Owl de servicios y carrusel Bootstrap de equipo/clientes con controles anterior/siguiente e indicadores. Se capturó al menos un estado “siguiente” de cada carrusel, sin activar destinos externos.
- Bloque Partner Zoho, sección de equipo, clientes, esencia, tarjetas de artículos recientes, formulario y footer.
- Las páginas secundarias conservan sus botones y enlaces en `page.json` por ruta.

## Formularios y widgets externos

- Formulario de contacto visible en portada, POST a Zoho CRM, con campos de contacto, captcha y seguimiento asociado. El inventario recoge método, action, nombres/tipos, etiquetas y required sin conservar valores ingresados.
- Se capturó su estado visual predeterminado. No se introdujeron datos ni se envió el formulario; por tanto, recepción, validación y retorno no se verificaron.
- La portada carga además un widget/chat y scripts de analítica externos. No se abrió ningún destino externo ni se inspeccionó su contenido.

## Otros comportamientos

- Los artículos enlazan desde tarjetas/listados a páginas individuales; esas rutas se recorrieron recursivamente.
- Links `mailto:`, `tel:`, fragmentos, descargas y esquemas especiales están en el inventario. No se activaron descargas, envío de correo ni llamadas.
- No se detectaron modales que requirieran apertura durante esta pasada; no se hizo entrada de datos o autenticación.

## Estado de verificación

Capturas, DOM, textos, botones, formularios y enlaces están por página bajo `docs/reference/`. Evidencia de interacciones adicionales: capturas `carousel-services-next-1440x900.png`, `carousel-team-next-1440x900.png` y `mobile-390x844-menu-open.png` donde existan. La prueba funcional completa queda pendiente para un entorno de staging con integración sandbox.
