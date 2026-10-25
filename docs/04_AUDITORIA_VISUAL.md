# 04 — Auditoría visual y responsive

## Evidencia

Playwright 1.61.1/Chromium 1228 inspeccionó la portada en 1440×900, 768×1024 y 390×844; capturas completas guardadas fuera del repositorio en `C:\Temp\gbitcorp-audit\home-desktop.png`, `home-tablet.png` y `home-mobile.png`. Todas respondieron HTTP 200.

| Viewport | scrollWidth / clientWidth | Alto de documento medido | Resultado |
|---|---:|---:|---|
| Móvil 390×844 | 405 / 390 | 6,629 px | Desborde horizontal de 15 px. Se observan áreas blancas amplias y contenido de blog/ensencia visualmente muy junto o solapado en la captura completa; confirmar elemento responsable en inspección de detalle. |
| Tablet 768×1024 | 768 / 768 | 6,493 px | Sin desborde horizontal global observado. |
| Escritorio 1440×900 | 1440 / 1440 | 6,950 px | Sin desborde horizontal global observado. |

La medición aplica al documento completo de la portada en esa sesión. Tres elementos `img` aparecieron completos con ancho natural cero y `src` vacío; podrían ser placeholders/lazy-load. Hay que inspeccionar sus atributos y estado visual antes de declarar imágenes rotas.

## Componentes y estilo observados

- Navegación superior con logo, menú y menú compacto en móvil.
- Hero con texto “Optimiza los procesos de tu negocio…”, CTA de contacto y fondo de ciudad.
- Líneas de negocio y acceso a diagnóstico; bloque de servicios en tarjetas; partner Zoho; sección de equipo/nosotros y clientes; esencia, artículos recientes, formulario de contacto y footer con contactos, navegación y redes.
- CSS fuente declara Noto Sans; el navegador también compone la pila Bootstrap/system UI. Paleta predominante azul corporativo (`#105180`, `#003756`, `#3e74ad`) con blanco y grises.
- Las secciones usan fondos PNG, incluidos `Fondo-Blanco-Curvas-03.png`, `Fondo-Gris-2.png`, `Fondo-de-Oficina-11.png`, `fondo-blanco6.png` y `Fondo-10.png`, con `background-position:center`/`background-size:cover` en estilos relacionados. Revisar escalado y recorte por breakpoint.
- Se aprecian carrusel/indicadores en la sección de servicios y animaciones declaradas por CSS/JS; no se enviaron acciones de formulario. Interacciones completas de menú/carrusel requieren validación funcional posterior.

## Problemas y riesgos visuales

- Overflow horizontal cuantificado en móvil: 15 px. Pendiente localizar nodo exacto y corregir en el nuevo diseño.
- La captura móvil muestra grandes huecos blancos entre secciones y bloques de contenido de esencia/blog próximos o superpuestos; es un hallazgo visual que necesita inspección DOM elemento por elemento para distinguir padding de fallo de maquetación.
- El formulario queda angosto respecto al viewport y el área de contacto consume mucho alto; verificar columnas, etiquetas, captcha e integración.
- Las imágenes usadas como fondos/divisores pueden recortarse o escalarse mal entre anchos. Mantener la intención mediante SVG/CSS responsive cuando sean decoración; conservar imágenes de marca con relación de aspecto y `object-fit` adecuados.
- No se validó un inventario completo de animaciones, focus/hover, todos los breakpoints ni todas las rutas a tres viewports. Las medidas responsive corresponden solo a la portada.

## Criterio para reconstrucción

Comparar por secciones a viewport equivalente; no replicar el desbordamiento ni superposiciones del original. Mantener jerarquía, tipografía, colores, fotografía y sentido de los separadores, a la vez que se reduce espacio vacío accidental y se garantiza lectura y navegación móvil.

## Ampliación de Fase 0.1

La medición inicial anterior cubría solo la portada y tres tamaños, con capturas temporales fuera del repositorio. La preservación exhaustiva posterior cubre 49 páginas en siete resoluciones y guarda las capturas permanentes, el contenido y las mediciones en `docs/reference/`. Sus resultados actualizados y los desbordamientos por página/tamaño están en [12_PROBLEMAS_RESPONSIVE.md](12_PROBLEMAS_RESPONSIVE.md); las capturas se enlazan desde cada `docs/reference/<ruta>/page.md`. Para los resultados de sitio completo, esa auditoría posterior reemplaza la limitación de cobertura indicada arriba.
