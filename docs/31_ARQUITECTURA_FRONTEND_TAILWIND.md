# 31 — Arquitectura del frontend con Tailwind CSS v4

**Estado:** diseño y planificación (FASE 2.1). No implementado.

**Alcance editorial:** las 49 rutas públicas preservadas son el universo de referencia; el manifiesto continúa siendo una allowlist candidata, no una autorización para importar o publicar.

## 1. Objetivos, límites y método

El frontend debe reconstruir el sitio público de `gbitcorp.com` con Django Templates, Wagtail y CSS compilado localmente, preservando su identidad y corrigiendo defectos técnicos de responsive, accesibilidad y carga. Modernizar la implementación no autoriza un rediseño.

Este informe es de análisis. No se instalaron paquetes, no se crearon templates/CSS/JavaScript, no se modificaron modelos o datos, no se copiaron assets y no se alteraron los originales. Las rutas bajo `docs/gbitcorp.com/` se consultaron solo en lectura; las capturas bajo `docs/reference/` son referencias locales ignoradas por Git y no se han alterado.

Se contrastaron los informes de auditoría, los modelos y bloques implementados, los templates/CSS originales y capturas de Home, blog, servicios y EULA. Este documento distingue:

- **Observado:** presente en código, informes o capturas.
- **Medido:** cifra tomada de un inventario o medición ya documentada, con el ámbito indicado.
- **Propuesta:** decisión de arquitectura para una fase posterior.
- **Pendiente:** requiere evidencia adicional o aprobación y no debe resolverse inventando contenido.

## 2. Inventario visual y comportamiento

### Sistema visual observado

El CSS principal de la versión corporativa nueva declara Noto Sans y contiene valores de marca dispersos, no un sistema de tokens. Entre los colores observados están `#105180` (títulos/azul), `#003756` (azul oscuro del footer), `#3e74ad` (acción principal), `#265e9b` (hover) y tonos `#8ba7cb`, `#a6b3ce`, `#c4dbf2`, `#a6c7e0`, además de grises y blanco. Su papel exacto varía por selector; la tabla de tokens los trata como candidatos rastreables al CSS, no como una nueva paleta.

La hoja corporativa declara Noto Sans, pero la carga externa de fuentes falló en la auditoría y la familia efectiva no quedó confirmada. El blog usa el conjunto CSS antiguo y se observa con Helvetica; EULA tiene un documento independiente con pila Inter/sistema. No se debe suponer una única tipografía efectiva para las tres variantes sin comprobación visual local/licencia.

Se observaron logo horizontal, barra superior y navegación, hero con foto urbana, tarjetas/columnas de servicios, secciones de socios y equipo, bloques de texto, tarjetas de artículos, formulario visual, tarjetas de herramientas y footer azul oscuro. EULA es una página legal autónoma y visualmente distinta, sin el header/footer corporativo.

### Breakpoints, composición y defectos

`site/templates/css/new/main.css` contiene reglas por rangos que incluyen 768–1024, 1025–1366 y desde 1367 px, además de reglas heredadas de Bootstrap 4.5.2. Se observan alturas rígidas, márgenes negativos y fondos escalados con `cover`. Son hechos del CSS legado; no constituyen por sí mismos un contrato que la nueva implementación deba replicar.

La auditoría responsive de las 49 páginas en siete viewports reporta overflow en 0/49 a 1920, 1440 y 1366; 3/49 a 1024 (máximo 82 px); 10/49 a 768 (máximo 320 px); 18/49 a 390 (máximo 689 px), y 18/49 a 375 (máximo 704 px). La portada presentó aproximadamente 15–16 px de desbordamiento, asociado al carrusel Owl y sus elementos clonados. En artículos se observaron imágenes flotantes y tablas anchas, incluidas tablas con estilo de Word; en móvil pueden exceder el viewport. En servicios se observó desbordamiento menor y listados de herramientas muy altos al apilarse. También hay grandes espacios vacíos en ciertas secciones móviles y recortes de divisores/fondos.

Las imágenes divisorias de secciones son prioritarias: conservar la intención de curva/onda, no la dependencia de una imagen de proporción rígida. Es viable evaluar CSS/SVG cuando el separador sea geométrico; mantener imagen optimizada para fotografía o ilustración con valor propio. La decisión se toma por recurso y comparación visual, no reemplazando todo indiscriminadamente.

### Interacciones públicas observadas

La auditoría registra navegación desktop/móvil, CTA, carruseles (Owl y carruseles Bootstrap heredados), filtro de categorías del blog, enlaces de compartir y un formulario público integrado externamente. El formulario no se envió durante la auditoría y su contrato de integración/respuestas no está confirmado. Los formularios deben tratarse como visuales sin envío hasta una fase de integración aprobada. No transferir identificadores, configuración o dependencias antiguas de widgets/analítica.

## 3. Design tokens propuestos

Los siguientes valores observados provienen de `docs/gbitcorp.com/site/templates/css/new/main.css` y de la auditoría visual `docs/04_AUDITORIA_VISUAL.md`; los valores por medir no se deben presentar como identidad confirmada.

| Token | Valor propuesto | Evidencia/estado |
|---|---|---|
| Azul de títulos | `#105180` | Observado en CSS original; validar usos exactos contra capturas. |
| Azul oscuro | `#003756` | Observado; usado en footer. |
| Azul de acción | `#3e74ad` | Observado en botones/acciones. |
| Hover de acción | `#265e9b` | Observado en CSS. |
| Tonos secundarios | `#8ba7cb`, `#a6b3ce`, `#c4dbf2`, `#a6c7e0` | Observados; mapeo semántico final pendiente. |
| Texto y superficies | grises observados, blanco | Varios valores (`#444444`, `#4d4d4d`, `#818181`, blanco); contrastar cada pareja. |
| Sans corporativa | Noto Sans | Familia declarada; disponibilidad, carga efectiva y licencia pendientes. |
| Blog | Helvetica/sans | CSS legado declara familia heredada; decidir si mantener variante visual. |
| EULA | Inter/system sans | Pila declarada en página independiente; validar renderizado. |
| Breakpoints | 48rem, 64.0625rem, 85.4375rem como candidatos | Inferidos de 768, 1025 y 1367 px del CSS a 16 px/rem; no fijar hasta probar. |
| Ritmo de espaciado | escala base 0.25rem como herramienta | Propuesta técnica, no escala observada. Ajustar a medidas/capturas. |
| Contenedor | límite por definir; probar ancho equivalente al Bootstrap legacy | Inferencia; medir capturas y texto antes de fijarlo. |
| Radio | 1rem en ciertos botones; avatar/icono circular | Observado en reglas concretas, no universal. |
| Sombras | navegación `0 2px 4px rgba(0,0,0,.1)`; formulario tiene sombra marcada | Observado. Reusar solo en componentes equivalentes. |
| Transiciones | botones alrededor de 0.3s; navbar declara 2.5s | Observado; transición larga debe evaluarse contra experiencia y movimiento reducido. |
| Z-index | valores bajos 1–2 en reglas observadas | Observado, insuficiente como escala semántica futura. Definir capas en implementación. |

Esbozo conceptual para evaluar en implementación; **no es un archivo CSS definitivo**:

```css
@import "tailwindcss";

@theme {
  --color-brand-blue: #105180;
  --color-brand-deep: #003756;
  --color-brand-action: #3e74ad;
  --color-brand-action-hover: #265e9b;
  --color-brand-muted: #8ba7cb;
  --font-sans: "Noto Sans", sans-serif;
  --breakpoint-md: 48rem;
  --breakpoint-lg: 64.0625rem;
  --breakpoint-xl: 85.4375rem;
}
```

Los breakpoints alteran qué utilidades responsivas existen y pueden divergir de los valores predeterminados de Tailwind; comparar antes de cerrar. Los colores secundarios, tipografías por variante, radios, sombras, spacing y contenedores requieren tokens adicionales solo después de medición. Los colores de texto deben superar evaluación de contraste; no inferir que un color de marca sobre cualquier fondo es accesible.

## 4. Arquitectura de templates Django/Wagtail

### Estructura propuesta

```text
templates/
├── base.html
├── includes/
│   ├── seo.html
│   ├── skip-link.html
│   ├── header.html
│   ├── navigation-desktop.html
│   ├── navigation-mobile.html
│   ├── footer.html
│   ├── pagination.html
│   └── messages-and-errors.html
└── editorial/
    ├── home_page.html
    ├── blog_index_page.html
    ├── blog_post_page.html
    ├── service_page.html
    ├── eula_page.html
    └── blocks/
        ├── home/
        └── service/
```

Es una propuesta de rutas, no archivos creados. La plantilla base tendrá los landmarks comunes para páginas corporativas; EULA conservará su composición autónoma con una base/documento legal específico, compartiendo solo lo que la evidencia justifique (por ejemplo, metadatos). Cada bloque StreamField tendrá una representación explícita y pequeña; usar `{% include_block %}` o `Meta.template` conforme al modelo y el patrón aprobado por Wagtail, sin HTML de contenido sin sanitizar. Componentes de tarjeta/CTA pueden ser includes con parámetros explícitos.

SEO debe usar los campos nativos Wagtail (`seo_title`, `search_description`) y un include de metadatos para title/description/canonical/OG cuando proceda. Canonical, imágenes OG y cualquier dato no cubierto por modelos se deben definir durante implementación sin añadir campos editoriales no aprobados. Navegación debe partir de rutas/manifiesto verificadas; no incorporar `django-wagtailmenus` sin una necesidad comprobada.

Paginación: el template puede usar paginación Django si la fase de implementación define el comportamiento, pero el código original tiene el markup de paginación comentado; no cambiar el comportamiento público sin aprobación. Categorías se presentan como filtros de listado, no como URLs públicas de detalle.

## 5. Mapa de componentes reutilizables

| Componente | Páginas/evidencia | Datos | Interacción | Responsive/accesibilidad | Estrategia |
|---|---|---|---|---|---|
| Header y navegación | Home/servicios (`header.php`), blog con header legacy (`header_old.php`) | enlaces públicos confirmados, logo | menú desplegable/móvil | teclado, foco visible, botón con `aria-expanded`, foco gestionado | include compartido con variante visual mínima si capturas lo requieren; no aplicar a EULA. |
| Hero | Home, blog index/artículo, servicios | texto/título; imagen de fondo o portada | CTA/enlaces según evidencia | texto real seleccionable, contraste sobre imagen, alto adaptable | include/bloque visual; fondo con focal point y fallback, no texto incrustado en imagen. |
| Botones/CTA | Home, servicios, blog, back-link EULA | etiqueta y destino | navegación | tamaño táctil, foco/hover, link semántico | include/clase de componente con estilo consistente por variante observada. |
| Enlaces a servicios | Home | título y `PageChooser` de ServicePage | navegación | tarjetas/links semánticos, orden | bloque existente `service_links`. |
| Carrusel/tarjetas de servicio | Home | bloque actual solo conserva grupos/imágenes; título/destino no modelados aquí | anterior/siguiente si se confirma | no permitir overflow de clones; controles etiquetados, teclado, sin autoplay o con pausa | componente discreto; **mismatch de datos pendiente** (ver §7). |
| Sección de socios/productos | Home | headings/imagen CTA definidos en PartnerSection | CTA opcional | apilar y mantener proporciones | template del bloque aprobado; recurso optimizado. |
| Sobre nosotros/equipo | Home | RichText, grupos de imágenes, careers link | CTA carreras | grupos reorganizados, alt contextual | bloque Home; imágenes responsive vía Wagtail. |
| Bloque de texto | Home | heading y RichText | enlaces del texto | anchura legible, headings jerárquicos | template asociado a `TextSectionBlock`. |
| Contacto/formulario visual | Home | el modelo actual conserva encabezado, no campos/servicio de envío | integración Zoho observada pero no verificada | labels, errores y estados si luego se implementa; no enviar en esta fase | presentar solo contenido confirmado; integración posterior separada y aprobada. |
| Lista de artículos | Blog index | páginas hijas live/publicadas, categorías, portada y resumen | filtro por categoría; enlaces a posts | grid que colapsa sin alturas rígidas; fallback sin JS | consulta hija filtrada y cards; no crear páginas de categoría. |
| Artículo | BlogPost | título, resumen, `body`, lead image, categorías | compartir/relacionados observados en legacy | texto legible; tablas/medios que no desborden | plantilla de artículo con body tipado; resolver brecha HTML antes de decidir fidelidad. |
| Ofertas de servicio | ServicePage | `offering` ordenado: título, icono, RichText | enlaces solo si respaldados | grid que colapsa de forma natural, alt | template de bloque `offering`. |
| Herramientas | ServicePage | StreamField de imágenes, orden | interacción no confirmada | tarjetas compactas, proporción controlada y alt | template de lista; no reproducir columna móvil excesivamente alta. |
| Footer | páginas corporativas; settings compartidos | dirección, teléfono, email, redes | enlaces externos/especiales documentados | landmarks, enlaces legibles, reflow | include que consume `SiteFooterSettings`; no incluir EULA salvo evidencia. |
| EULA | ruta EULA | RichText legal literal | back-link | columna fluida, zoom/lectura, headings | template autónomo sobrio; no header/footer corporativo. |
| Estados 404/500 | respuesta del sitio nuevo | contenido mínimo de sistema | volver/navegar | status HTTP correcto, salida accesible | templates de error, sin inventar rutas editoriales. |

No hay evidencia para añadir nuevos componentes de testimonios, pricing, newsletter u otros patrones no preservados.

## 6. Correspondencia modelos → templates y StreamField

| Modelo/bloque actual | Template/representación prevista | Estado y observaciones |
|---|---|---|
| `HomePage` | `editorial/home_page.html` | Hero y secciones ordenadas; conservar secuencia editorial. Campo de imagen/CTA de hero no está en el modelo actual. |
| `ServiceLinksSectionBlock` | bloque home “enlaces de servicio” | Título/links a ServicePage; no confundir con carrusel de servicios. |
| `ServiceCarouselSectionBlock` + `ImageGroupBlock` | bloque home de tarjetas/carrusel | Solo grupos de imágenes. El código/preservación muestra tarjetas con nombre/enlace: falta confirmar cómo se recuperan esos datos. No inferir texto desde nombre de archivo ni cambiar modelo aquí. |
| `PartnerSectionBlock` | bloque home de socios/productos | Heading, imágenes y CTA disponibles. |
| `AboutSectionBlock` | bloque home “sobre nosotros” | RichText, grupos de imágenes y careers link. |
| `TextSectionBlock` | bloque de texto genérico acotado | Heading + RichText. |
| `ContactSectionBlock` | encabezado/sección visual de contacto | No representa el contrato de envío Zoho. |
| `BlogIndexPage` | `editorial/blog_index_page.html` | Imagen header y cards de hijos; búsqueda/filtro categoría sin URLs nuevas. Paginación pendiente por comportamiento legacy. |
| `BlogPostPage` | `editorial/blog_post_page.html` | Título, resumen, body StreamField, lead image, M2M categoría. `rich_text` está limitado a headings, énfasis, listas, links; el legado público tiene tablas e imágenes/floats. Requiere resolución editorial/técnica antes de migrar contenido con esas formas. |
| `ServicePage` | `editorial/service_page.html` | Banner/description; `offering` y tools StreamField, respetando orden. |
| `EulaPage` | `editorial/eula_page.html` autónomo | RichText con allowlist, texto legal no se reescribe. |
| `RouteContainerPage` | sin template público; descendientes resuelven ruta | Debe continuar 404 directo y no aparecer en navegación/sitemap conforme a las pruebas/modelo. |
| `BlogCategory` | snippet en filtro/listado | No template de página/detalle; usar solo las categorías públicas confirmadas cuando exista aprobación de contenido. |
| `SiteFooterSettings` | `includes/footer.html` | Setting compartido; consume valores administrables, mostrar solo valores aprobados/configurados. |

Las cinco familias editoriales están cubiertas: Home, índice/artículo de blog, servicio y EULA. El ancestro estructural no es contenido editorial adicional. El manifiesto contiene 49 URLs (1 Home, 1 blog index, 42 posts, 4 servicios, 1 EULA); la arquitectura no crea ni autoriza instancias.

## 7. Hallazgos de compatibilidad modelo/diseño

1. **Hero Home:** el modelo actual incluye `hero_copy`, pero no expresa una relación visible con el gran fondo urbano ni CTA principal. El CSS legado coloca imagen y acciones visuales. Determinar en FASE 2.2 si el fondo es recurso estático versionado, imagen administrada, o si hay que proponer cambio contractual; requiere validar si el CTA está respaldado por datos ya modelados. No inventar.
2. **Carrusel Home:** `ServiceCarouselSectionBlock` aporta imágenes, pero la composición pública muestra tarjetas con títulos/enlaces. Hay una brecha de datos confirmada entre el bloque implementado y la referencia; identificar fuente real/decisión antes del template final.
3. **Cuerpo de artículos:** StreamField actual permite RichText acotado. La auditoría responsive registra tablas anchas y elementos de imagen/flotantes en artículos públicos. No renderizar HTML ProcessWire bruto. Antes de importación, decidir bloques tipados suficientes (p. ej. imagen, tabla tratada, texto) o conversión intermedia con validación, en proceso contractual aparte.
4. **Contacto:** el bloque modela encabezado, no campos. El formulario público se conectaba a un tercero y no se envió. La representación estética no implica autorización ni datos suficientes para integrar Zoho.
5. **Blog:** evitar pagination nueva hasta aprobación; markup de paginación original estaba comentado. Mantener filtros sin publicar rutas de categoría.

Estos hallazgos no se corrigen en esta fase: el prompt prohíbe cambios de modelos.

## 8. Recursos visuales y gestión

El inventario vigente documenta 933 instancias de recursos y 239 referencias URL/tipo; 226 tienen archivo local asociado y 13 no localizados en el respaldo. El inventario ProcessWire incluye 728 archivos en total, de los cuales no todos están confirmados como vigentes. Esas cifras describen universos distintos; no copiar ni publicar el conjunto completo. Las referencias no localizadas no se consideran automáticamente rotas.

Recursos Home prioritarios de `docs/14_DIAGNOSTICO_HOME_RENDIMIENTO.md` (dimensiones/pesos reportados por la inspección):

| Recurso original relativo | Uso observado | Tratamiento propuesto |
|---|---|---|
| `site/templates/img/new/Ciudad-Fondo.png` (3126×3909; ~5.05 MB) | fondo hero | revisar crop/focal point y conversión/tamaños; priorizar solo si confirmado arriba del pliegue. |
| `site/templates/img/new/services/Fondo-Blanco-Curvas-03.png` (7967×5705; ~786 KB) | separador/curva | evaluar reconstrucción CSS/SVG responsive; no trasladar imagen de gran dimensión sin necesidad. |
| `site/templates/img/new/partner/Fondo-Gris-2.png` (1913×1091; ~81 KB) | fondo/sección | verificar si es geometría reemplazable; conservar intención tonal. |
| `site/templates/img/new/us/Fondo-de-Oficina-11.png` (4000×2000; ~2.04 MB) | foto de oficina | fotografía con valor propio: conservar como candidato, optimizar renditions y punto focal. |
| `site/templates/img/new/customer/fondo-blanco6.png` (1913×1091; ~113 KB) | curva de sección | evaluar SVG/CSS frente a imagen. |
| `site/templates/img/new/blog/Fondo-10.png` (3600×1810; ~519 KB) | fondo/divisor del blog | el alto móvil observado resulta desproporcionado; preferir divisor flexible y tarjetas de altura natural. |
| `site/templates/img/new/contact/fondo-6.png` (2124×1122; ~394 KB) | fondo contacto | determinar si fotográfico/decorativo; sin alturas fijas, considerar variante responsive. |

Se reportaron también fotos de equipo/carruseles de tamaño alto, logos con dimensiones fuente mucho mayores que su visualización y una imagen fallback grande. Confirmar cada uso en las capturas antes de selección final.

**Estrategia propuesta:** logo, iconos de marca y geometrías pequeñas estables pueden ser staticfiles versionados tras seleccionar/autorizar el asset exacto; fotos, imágenes editoriales y documentos públicos deben administrarse en Wagtail y servirse mediante renditions. En plantillas usar `picture`/`img` con `srcset` cuando haya renditions útiles, dimensiones intrínsecas para reservar espacio, alt contextual y `loading="lazy"` bajo el pliegue. Priorizar únicamente imagen hero comprobada; no hacer lazy-load de la imagen LCP visible. Fuentes solo después de confirmar licencia y disponibilidad; evitar depender de una fuente remota que falló.

## 9. Responsive y JavaScript

### Responsive

Adoptar mobile-first, contenido que determina la altura, `min-width:0` en ítems de grid/flex, imágenes con ancho máximo y proporción controlada, tablas tratadas con alternativa legible, y contenedores con padding fluido. El menú se transforma a navegación móvil en el punto validado visualmente, no por copiar todos los cortes Bootstrap. Las tarjetas y columnas se apilan sin ocultar contenido; imágenes decorativas deben conservar focal point/curva y no causar ancho del documento. No usar heights fijas para compensar contenido ausente.

La matriz de comprobación conservará los siete viewports preservados: 1920×1080, 1440×900, 1366×768, 1024×768, 768×1024, 390×844 y 375×812. Añadir viewport de breakpoint únicamente si la implementación demuestra un salto problemático. Criterio mínimo: sin scroll horizontal de documento, contenido no recortado, tipografía y orden equivalentes a la intención original, sin superposición.

### JavaScript

Preferir HTML nativo para enlaces, detalles y navegación. JavaScript modular nativo solo para menú móvil, filtro de categorías y carrusel si no hay alternativa CSS/native adecuada. Usar `button` real, `aria-expanded`, Escape/cierre, gestión de foco y estado visible. Evitar jQuery, Owl y clones; no autoplay salvo requisito demostrado y controles de pausa. Animación debe respetar `prefers-reduced-motion`.

Formulario: no enviar, conectar ni simular contrato externo hasta aprobación de integración. Validación funcional, captcha, privacidad, estados/respuestas y protección antiabuso requieren especificación separada. No crear endpoints ni exponer configuración antigua.

## 10. Accesibilidad, rendimiento y SEO

- Estructura semántica con header/nav/main/footer, landmarks únicos, enlaces con propósito, un H1 significativo por vista y secuencia de headings coherente.
- Salto a contenido, navegación completa por teclado, foco visible no oculto por el header, menú anunciado y operable, controles táctiles adecuados.
- Medir contraste de texto, CTA, estados hover y foco contra superficies reales; no inferir cumplimiento por nombre/color de marca.
- Alt depende de función: texto alternativo descriptivo para imagen informativa; `alt=""` para decoración; no usar nombre de archivo.
- Respetar movimiento reducido; evitar carruseles automáticos y transiciones largas sin evaluar necesidad.
- Usar renditions optimizadas y tamaños por breakpoint; definir `width`/`height` para evitar CLS; prioridad alta solo para LCP confirmado; lazy-load imágenes bajo pliegue.
- Minimizar JS y CSS de terceros, evitar cargar icon fonts/frameworks completos cuando pocos iconos/estilos basten. No hay datos suficientes para fijar presupuesto de bytes; medir baseline en FASE 2.2 antes de acordar un límite.
- SEO: título/descripción Wagtail, canonical, Open Graph cuando haya datos validados, URLs existentes y estados HTTP apropiados. No generar rutas por categorías ni cambiar slugs.

## 11. Integración propuesta de Tailwind CSS v4

### Archivos y flujo

No hay actualmente configuración de Node/package ni CSS público nuevo. Propuesta para FASE 2.2:

```text
package.json / lockfile
frontend/src/css/site.css       # @import y @theme
static/compiled/site.css        # salida generada, no edición manual
static/js/                       # módulos propios mínimos
templates/                       # Django/Wagtail escaneados por Tailwind
```

Instalar luego, con versiones estables y lockfile, `tailwindcss` y `@tailwindcss/cli`; desarrollar con CLI `--watch` y compilar salida estática de producción en build. Servir la salida por Django staticfiles usando `{% load static %}` y nombre namespaced, y ejecutar `collectstatic` en despliegue. No CDN en producción ni `django-tailwind` por defecto. La configuración final de compilación debe respetar Windows local y ser reproducible en Docker/Linux posterior.

Tailwind v4 usa `@import "tailwindcss"`, tokens CSS `@theme` y detección de clases por escaneo de archivos. Como ProcessWire y `docs/reference/` son ignorados/no versionables, delimitar explícitamente fuentes de templates y no escanear respaldo, `.venv`, lockfiles o referencias. Si se usa `@source`, fijar base/rutas desde la ubicación real del CSS. Las clases deben aparecer completas y estáticas en templates/código; no construir nombres como `text-{{ color }}` desde valores Wagtail. Mapear opciones editoriales a clases allowlist predefinidas.

El CSS compilado será generado (decidir en 2.2 si se ignora y se compila en CI/build o se versiona; se recomienda ignorar artefacto reproducible y compilar en despliegue). No versionar node_modules, cachés ni archivos temporales. No se instalaron Node, Volta, Tailwind ni paquetes durante esta fase.

### Comandos conceptuales (no ejecutados)

Una vez aprobada la fase y confirmada la versión de Node ya disponible por Volta:

```powershell
npm run css:watch
npm run css:build
uv run python manage.py runserver 127.0.0.1:8000
```

Los scripts `css:watch`/`css:build` y los nombres de paquete aún no existen: se deben definir al implementar, no copiar estos comandos como ejecutables actuales.

## 12. Validación visual futura con Playwright

Las capturas de referencia están en `docs/reference/` y se generaron en la FASE 0.1: 49 páginas × siete viewports = 343 capturas de base, además de estados interactivos que explican el total de 351. El directorio es material local ignorado; este informe no copia capturas. Casos consultados visualmente incluyen:

- `docs/reference/home/desktop-1440x900.png`, `tablet-768x1024.png`, `mobile-390x844.png` y `audit-loaded-full-mobile-390x844.png`.
- `docs/reference/blog/posts/desktop-1440x900.png` y capturas desktop/mobile de artículos.
- Capturas desktop/mobile de `docs/reference/negocio/outsourcing-bi/business-inteligence/`.
- `docs/reference/eula/quickbook/desktop-1440x900.png` y `mobile-390x844.png`.

La ruta exacta/nombre de cada archivo debe verificarse en el entorno local antes de ejecutar comparación; las referencias no son parte de Git ni de CI. FASE 2.2 debe usar Playwright ya instalado por Volta, mismo navegador, viewport, fonts, escala y estado de contenido para origen/reconstrucción. Capturar páginas completas y estados relevantes (menú móvil abierto, filtro, carrusel controlado); nunca enviar formulario. Medir overflow, imágenes cargadas/dimensiones, consola/HTTP, layout shift, títulos y focal points. Comparar por regiones/componentes y con tolerancia para rasterizado/fonts; una diferencia pixel-perfect no es por sí sola regresión. Toda desviación visual significativa debe documentarse y aprobarse.

Las capturas de baseline locales son útiles pero no portables; si se requiere CI visual, decidir una política de almacenamiento de fixtures autorizados sin incluir ProcessWire ni datos sensibles.

## 13. Riesgos y decisiones pendientes

| Tema | Estado | Siguiente decisión |
|---|---|---|
| Tipografía corporativa efectiva y disponibilidad/licencia | Pendiente | confirmar archivo/licencia/fallback y comparar localmente; no depender de Google Fonts fallida. |
| Datos de hero Home (imagen/CTA) | Brecha confirmada | cotejar preservación/modelo; contrato editorial si requiere campos nuevos. |
| Títulos/links de carrusel Home | Brecha confirmada | identificar datos públicos exactos y decidir si contrato/modelo necesita ajuste. |
| Estructuras HTML de artículos | Riesgo confirmado | definir tratamiento seguro para tablas e imágenes; revisión editorial antes de importar. |
| Formulario/Zoho | Integración no verificada | especificación de privacidad, destino, captcha, estados y credenciales fuera de esta fase. |
| Paginación blog | No observada como activa | no introducir cambio sin aprobación. |
| Assets faltantes (13 referencias) | Pendiente, no necesariamente rotos | clasificar uno por uno si los necesita el template actual. |
| Fuentes, iconos y dependencias legacy | Parcial | conservar solo uso comprobado/licencia; evitar copiar Bootstrap/jQuery/Owl completos. |
| Tokens spacing/container/contraste | Propuesta parcial | medir y verificar con captura y herramienta de contraste en 2.2. |
| Comparación visual en CI | Limitación de referencias | definir custodia de baseline o mantener validación local reproducible. |

No hay bloqueo para comenzar el andamiaje de templates/CSS de componentes confirmados, pero **hero, carrusel y cuerpo de artículo requieren decisión antes de cerrar esas vistas o importar contenido**. Cambios de modelo están fuera de alcance de este informe y requieren autorización.

## 14. Plan de implementación FASE 2.2

1. Confirmar aprobación de arquitectura y resolver si las brechas Home/artículo requieren volver al contrato/modelos; mantener modelos sin cambios si no hay necesidad demostrada.
2. Verificar Node/Volta y Playwright existentes mediante instrucciones locales, sin reinstalarlos; registrar versiones. No instalar hasta que esta fase de implementación esté aprobada.
3. Seleccionar, con inventario 23 y evidencia de referencia, un conjunto mínimo de assets autorizados; confirmar fuentes/licencias y variantes. No copiar el respaldo completo.
4. Crear package manifest/lock y Tailwind CLI v4 estable; CSS de entrada con tokens aprobados y rutas explícitas de escaneo; scripts de watch/build; ignorar artefactos y dependencias.
5. Implementar la base corporativa, metadata, header/nav desktop+móvil y footer; mantener variante visual del blog si las capturas la respaldan; EULA independiente.
6. Crear templates por modelo y templates de bloques StreamField existentes, respetando orden y usando HTML semántico. No crear contenido ni publicar páginas.
7. Implementar componentes Home, blog/listado/artículo, servicio y EULA; formulario solo visual salvo integración aprobada. Resolver tablas/medios con contrato seguro, nunca HTML crudo.
8. Añadir JS mínimo y accesible para navegación/filtro/carrusel que realmente se mantenga; sin autoplay/clones ni envío real.
9. Integrar imágenes con renditions Wagtail, tamaños y alt; corregir divisores responsivos y overflow; respetar contenido variable.
10. Validar accesibilidad, SEO, rutas/errores, rendimiento y las 49 rutas en siete viewports con Playwright. Comparar contra baseline local; revisar cada discrepancia de identidad visual y documentar excepciones.
11. Documentar comandos Windows/Volta, build/collectstatic y diferencias Linux/Docker futuras; sin crear Dockerfile en esta fase salvo alcance aprobado por separado.

## 15. Criterios de aceptación de esta arquitectura

- Las cinco familias de páginas editoriales están mapeadas; las 49 URLs públicas siguen siendo el alcance y no se crean rutas nuevas.
- Los componentes repetidos se representan una vez y los elementos específicos de EULA/blog no se fuerzan a una plantilla visual inapropiada.
- Tokens trazan a CSS/capturas o están etiquetados como inferidos/pendientes.
- No se copia Bootstrap ni otro framework heredado completo.
- Las imágenes divisorias tienen estrategia por recurso; se conserva fotografía/ilustración valiosa y se corrigen recortes/overflow.
- El contrato de formulario externo no se inventa ni ejecuta.
- Tailwind se compila localmente, sin CDN en producción ni clases construidas dinámicamente desde contenido.
- Todos los cambios visuales significativos se someten a aprobación; mejoras técnicas conservan apariencia intencional.
- Playwright valida las 49 rutas y viewports preservados sin tocar los materiales de referencia.
- No se importan contenido ni assets históricos sin aprobación explícita.

## Referencias

### Locales del proyecto (solo lectura)

- `docs/04_AUDITORIA_VISUAL.md`, `docs/07_PRESERVACION_SITIO.md`, `docs/08_INVENTARIO_COMPLETO_URLS.md`, `docs/09_CONTENIDO_PAGINAS.md`, `docs/11_INTERACCIONES_Y_FUNCIONALIDADES.md`, `docs/12_PROBLEMAS_RESPONSIVE.md`, `docs/14_DIAGNOSTICO_HOME_RENDIMIENTO.md`.
- `docs/21_MANIFIESTO_CONTENIDO_VIGENTE.csv`, `docs/23_INVENTARIO_ASSETS_VIGENTES.md`, `docs/25_CIERRE_AUDITORIA_PROCESSWIRE.md`.
- `docs/27_CONTRATO_EDITORIAL_WAGTAIL.md`, `docs/28_RESOLUCION_DECISIONES_EDITORIALES.md`, `docs/29_IMPLEMENTACION_MODELOS_WAGTAIL.md`, `docs/30_VALIDACION_EDITORIAL_WAGTAIL.md`.
- Código leído: `docs/gbitcorp.com/site/templates/header.php`, `footer.php`, `home.php`, `blog-posts.php`, `blog-post.php`, `service_service.php`, `eula.php`, `css/new/main.css` y CSS/headers legacy pertinentes.
- Capturas locales: rutas enumeradas en §12. No versionadas y no modificadas.

### Documentación oficial consultada

- Tailwind CSS v4 CLI: <https://tailwindcss.com/docs/installation/tailwind-cli>
- Tailwind theme variables: <https://tailwindcss.com/docs/theme>
- Tailwind source detection: <https://tailwindcss.com/docs/detecting-classes>
- Wagtail 7.4 StreamField: <https://docs.wagtail.org/en/v7.4/topics/streamfield.html>
- Wagtail 7.4 image handling: <https://docs.wagtail.org/en/stable-7.4.x/topics/images.html>
- Django 5.2 static deployment: <https://docs.djangoproject.com/en/5.2/howto/static-files/deployment/>
- Playwright visual snapshots: <https://playwright.dev/docs/test-snapshots>
