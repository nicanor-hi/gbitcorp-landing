# 12 — Problemas responsive

El diagnóstico de Home añade captura de carga temprana vs completa, dimensiones/recorte de fondos `cover` y causas de imagen de alto costo: [14_DIAGNOSTICO_HOME_RENDIMIENTO.md](14_DIAGNOSTICO_HOME_RENDIMIENTO.md). La medición de 390×844 de esta revisión volvió a observar 15 px de overflow horizontal.

## Método y matriz

Se midió `document.documentElement.scrollWidth` frente a `clientWidth` por página, tras cargar y recorrer el documento, en 49 páginas y estos viewports: 1920×1080, 1440×900, 1366×768, 1024×768, 768×1024, 390×844 y 375×812. Resultados por ruta/tamaño y nodos que exceden viewport: [reference/responsive.csv](reference/responsive.csv) y [reference/responsive.json](reference/responsive.json).

| Viewport | Páginas con overflow | Máximo medido | Observación |
|---|---:|---:|---|
| 1920×1080 | 0/49 | 0 px | Sin overflow global medido. |
| 1440×900 | 0/49 | 0 px | Sin overflow global medido. |
| 1366×768 | 0/49 | 0 px | Sin overflow global medido. |
| 1024×768 | 3/49 | 82 px | Imágenes de artículos exceden el contenedor. |
| 768×1024 | 10/49 | 320 px | Imágenes fijas y tablas de contenido. |
| 390×844 | 18/49 | 689 px | Imágenes de artículos, flotantes laterales y tablas anchas. |
| 375×812 | 18/49 | 704 px | Mismos patrones; algunos excesos aumentan con el ancho menor. |

La portada por sí sola presenta 15 px a 390 px por elementos/clones del carrusel Owl fuera de viewport; a 375 px registra 16 px. Las rutas de servicio principal no presentan overflow a móvil salvo la página de Gestión Documental, que presenta 44 px a 390 y 59 px a 375; el CSV permite identificar nodos cuando se exponen.

## Causas identificadas

- Imágenes dentro de artículos conservan dimensiones intrínsecas grandes y clases `align_left`/`align_right`, sin ajuste suficiente al ancho de móvil. Ejemplos: `smartqa-una-iniciativa-gbit` llega a 689 px de exceso a 390; `error-defecto-y-fallo` a 617 px; `implementar-la-digitalizacion-masiva-de-documentos` a 646 px.
- Contenido pegado desde documentos contiene tablas `MsoTableGrid` de 800 px y celdas/imágenes fijas. Por ejemplo, `moneyball-el-arte-de-ganar-un-juego-injusto` excede 431 px a 390 y 446 px a 375.
- En la portada, las diapositivas clonadas del carrusel Owl sobresalen visualmente del viewport aunque el exceso global medido sea menor que el tamaño de esas diapositivas.
- En 1024 px algunos artículos aún tienen imágenes de 992–1,064 px que exceden el contenedor.
- Elementos como tablas, imágenes alineadas y contenido HTML heredado no necesariamente aparecen en la plantilla compartida; el arreglo requiere normalizar el HTML/editor de artículos además del CSS.

## Imágenes divisoras y fondos

En portada hay fondos/separadores con recursos como `Fondo-Blanco-Curvas-03.png`, `Fondo-Gris-2.png`, `Fondo-de-Oficina-11.png`, `fondo-blanco6.png` y `Fondo-10.png`, aplicados a secciones por CSS. Se observan como parte del diseño de servicios, partner, equipo/clientes, esencia y blog. La captura permite comparar su intención, pero este barrido no identificó desbordamiento global atribuible a todos los fondos.

Para la implementación se recomienda reconstruir geometrías decorativas con pseudo-elementos, gradientes o SVG escalable. Para fotografía/marca, usar `picture`/`img`, `object-fit`, focal points y variantes por breakpoint. Evitar fondos PNG de gran ancho para dibujar curvas decorativas y no ocultar contenido para suprimir el overflow.

## Hallazgos visuales adicionales

- Capturas móviles muestran grandes zonas blancas entre secciones de portada y el bloque esencia/blog visualmente apretado; revisar composición por breakpoint al reconstruir.
- No se detectó overflow en escritorio en las 49 rutas, pero ello no garantiza que todos los elementos tengan legibilidad/tamaño óptimo.
- Las capturas son de página completa; cada registro está enlazado desde su ficha en `docs/reference/<ruta>/page.md`.

## Pendiente para la nueva implementación

- Limitar imágenes de rich text con `max-width:100%; height:auto`, retirar anchos inline heredados y definir estilos de flotado que colapsen a una columna en móvil.
- Hacer tablas horizontales desplazables dentro de un contenedor accesible o convertirlas en bloques responsivos si su semántica lo permite.
- Recortar/ocultar clones fuera del área visible del carrusel sin crear scroll en `body`; revisar foco y controles táctiles.
- Verificar todas las rutas y siete resoluciones después de migrar contenido a Wagtail.
