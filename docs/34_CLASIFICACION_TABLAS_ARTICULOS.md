# 34 — Clasificación semántica de tablas de artículos

**Fase:** 2.2A.2 — análisis y documentación.
**Estado:** clasificación preliminar basada en estructura restringida y capturas preservadas; no se transformó contenido ni se modificó esquema.

## Alcance, método y límites

Se inspeccionaron exclusivamente las doce etiquetas `<table>` de los cinco artículos públicos A incluidos en `docs/33_AUDITORIA_HTML_ARTICULOS.md` (IDs 1080, 1641, 1667, 1669 y 1670). El contenido se consultó mediante `SELECT` con `pw_auditor` en `127.0.0.1:3307`; los metadatos de conexión confirmaron MySQL 8.4.4, puerto 3307, base local `processwire_gbitcorp_local` e identidad `pw_auditor@127.0.0.1`. El SQL no escribió en la base.

El helper convirtió el cuerpo únicamente en memoria y guardó en `%TEMP%` una salida estructural: cantidad y orden de tablas, filas/celdas, encabezados sintácticos, clases, atributos de ancho, celdas vacías, longitudes de texto, presencia de imágenes/enlaces y etiquetas internas. No guardó texto de celdas ni cuerpos HTML en el repositorio. Se eliminaron los archivos temporales de credenciales; no quedó archivo CNF temporal.

La inspección visual utilizó las capturas preservadas desktop y móvil de `docs/reference/blog/posts/` para los cinco artículos. El parser fue Python `html.parser`, no un parser HTML5 ni el DOM del navegador. En particular, identificó anidamiento en dos tags del artículo 1080. Esto puede reflejar HTML anidado real o recuperación distinta del navegador; no se instaló una dependencia para resolverlo. Por eso esos dos casos quedan ambiguos. Las celdas no se exportaron ni se transcribieron.

En la matriz, “fila × celdas” es el conteo sintáctico del extractor. La clasificación interpreta conjuntamente ese conteo, la estructura resumida de etiquetas (sin valores) y la composición visible; no equivale a validar cada celda del DOM reparado por un navegador.

## Matriz de las doce tablas

| ID / ruta pública | Posición | Evidencia estructural no textual | Contraste visual preservado | Clasificación | Confianza y decisión editorial |
|---|---:|---|---|---|---|
| 1080 `/blog/posts/como-asegurarse-que-los-servicios-de-cloud-computing-sean-eficientes/` | 1 | 1×1; una celda con encabezado `h5` y `div`; sin clase de tabla, imagen ni enlace detectado | El artículo presenta contenido editorial e ilustraciones; no se observa una cuadrícula de datos | Tabla de maquetación | Media. Una sola celda y encabezado interno no ofrecen relación fila/columna; conservar como RichText/encabezado, no TableBlock. |
| 1080 misma ruta | 2 | 1×1 según parser; celda sin texto contado y etiqueta `tbody`; el extractor detectó otra tabla anidada | No hay evidencia visual de datos tabulares | Ambigua / requiere revisión | Baja. Confirmar el cierre/anidamiento con DOM HTML5 si este artículo se convierte; no migrar como tabla hasta resolver. |
| 1080 misma ruta | 3 | 1×1; anidada según parser; una celda con `h5` y `div`; sin imagen/enlace | No se distingue una relación tabular de datos en la captura | Ambigua / requiere revisión | Baja. El anidamiento reportado hace inseguro inferir semántica; analizar junto a la tabla 2 con DOM reparado. |
| 1080 misma ruta | 4 | 1×1; una celda contiene varios párrafos; sin encabezados de tabla, imágenes ni enlaces | Se visualiza como contenido corrido del artículo | Tabla de maquetación | Media. Convertir contenido a RichText respetando orden; descartar la envoltura de tabla tras validar DOM. |
| 1641 `/blog/posts/smartqa-una-iniciativa-gbit/` | 1 | 1×3; `MsoTableGrid`; primera celda con párrafo, segunda vacía y tercera con imagen/párrafos; sin `th`, caption o enlaces | Texto y conjunto de logos/recursos aparecen compuestos en columnas | Tabla de maquetación | Alta. Es composición texto–espaciador–imagen, no datos relacionados. Transformar en layout responsive de texto e imagen; no usar TableBlock. |
| 1667 `/blog/posts/una-app-para-tu-negocio-considera-una-pwa-entre-tus-opciones/` | 1 | 2×2; `MsoTableGrid`; primera fila contiene texto breve destacado en ambas celdas; segunda fila contiene listas ordenadas; sin `th`, caption, imagen ni enlace | La captura muestra comparación en dos columnas de instrucciones/plataformas | Tabla de datos / comparación | Alta para intención comparativa; media para semántica de encabezados. Modelar como comparación accesible con encabezados explícitos tras revisión editorial; preservar listas y orden. |
| 1667 misma ruta | 2 | 2×2; `MsoTableGrid`; primera fila contiene texto destacado; segunda fila listas no ordenadas en ambas celdas; sin `th`, caption, imagen ni enlace | La captura muestra contraste de dos experiencias en columnas y listas | Tabla de datos / comparación | Alta para intención comparativa; media para asignar encabezados. Preferir representación semántica accesible que conserve el contraste; no importar literalmente estilo Word. |
| 1669 `/blog/posts/moneyball-el-arte-de-ganar-un-juego-injusto/` | 1 | 1×3; `MsoTableGrid`; primera celda con párrafo, segunda vacía, tercera con imagen; sin `th`, caption; ancho fijo de 800 px documentado en auditoría responsive | Captura de escritorio muestra texto junto a imagen; móvil acusa desbordamiento horizontal | Tabla de maquetación | Alta. Sustituir la tabla por composición fluida de texto e imagen. No reproducir el ancho fijo ni conservarla como datos. |
| 1670 `/blog/posts/smart-control-sistema-de-marcacion-y-control-de-esfuerzo/` | 1 | 1×2; primera celda imagen, segunda texto con párrafos/énfasis; sin clase Word, `th`, caption o enlace | Captura muestra imagen y explicación en columnas | Tabla de maquetación | Alta. Layout de contenido con imagen, apilable en móvil; imagen requiere decisión editorial de alt. |
| 1670 misma ruta | 2 | 1×2; imagen en primera celda, varios párrafos en segunda; sin semántica de tabla de datos | Composición repetida de imagen y explicación | Tabla de maquetación | Alta. Mismo patrón responsive que tabla 1, manteniendo orden observado. |
| 1670 misma ruta | 3 | 1×2; imagen en primera celda, párrafos en segunda; sin `th`, caption ni enlaces | Composición repetida imagen/texto | Tabla de maquetación | Alta. Mismo patrón; no crear bloque de tabla. |
| 1670 misma ruta | 4 | 1×2; imagen en primera celda, párrafos/énfasis en segunda; sin `th`, caption ni enlaces | Composición repetida imagen/texto | Tabla de maquetación | Alta. Mismo patrón; verificar en implementación que la imagen no quede rígida o desbordada. |

### Resultado agregado

- **12** tags `<table>` en total.
- **8** clasificados como tablas de maquetación con evidencia suficiente para recomendar eliminar la envoltura tabular.
- **2** tablas comparativas en el artículo PWA; su intención de comparación es clara, pero el HTML no declara `th` y requiere revisión editorial de encabezados antes de convertir.
- **2** casos ambiguos del artículo 1080, debido a anidamiento detectado por parser no HTML5 y falta de semántica de datos visible.
- No se detectaron `th`, `caption`, `rowspan` ni `colspan` en las doce estructuras inspeccionadas. Esto describe el parseo sintáctico, no garantiza el DOM final del navegador.

## Recomendación para la representación editorial

1. Mantener RichText restringido para párrafos, encabezados y listas que sean contenido. Las tablas 1 y 4 de ID 1080 parecen envolturas de contenido; las tablas 2 y 3 esperan resolución de HTML antes de cualquier conversión.
2. Para IDs 1641, 1669 y 1670, extraer contenido, imagen y orden a bloques de imagen/RichText y presentarlos con layout CSS responsive. No modelar columnas de maquetación como tabla editorial ni preservar anchos heredados.
3. Las dos estructuras de ID 1667 expresan comparaciones, pero el origen usa filas/celdas ordinarias con texto destacado, no encabezados HTML semánticos. Tras aprobación editorial, convertirlas a una representación semántica tipada con encabezados/filas accesibles; en móvil puede presentarse como pares de tarjetas o filas apiladas, conservando claramente a qué encabezado pertenece cada lista. No reducir la comparación a RichText plano ni habilitar HTML arbitrario.
4. Estos hallazgos son evidencia para el contrato futuro, no aprobación para modificar `BlogPostPage`, crear bloques/migraciones o importar artículos. La conversión de las dos tablas comparativas y los casos ambiguos requiere control editorial y pruebas de contenido.

## Riesgos y pendientes

- **No bloquea la arquitectura general del frontend:** ocho tablas tienen evidencia suficiente de maquetación y pueden convertirse mediante composición responsive cuando se autorice una fase de contenido.
- **Bloquea conversión automática segura de las dos tablas PWA:** falta aprobación editorial de los textos que deben ser encabezados de cada comparación y validación de accesibilidad de la representación.
- **Pendiente para las dos tablas del artículo 1080:** obtener DOM HTML5/resuelto y confirmar si son tablas anidadas reales o una reparación sintáctica; sin eso no debe ejecutarse una conversión automática.
- El parser disponible no recupera HTML5 del mismo modo que un navegador. No se instaló `html5lib`/`lxml` ni se modificaron dependencias.
- Las capturas disponibles apoyan la interpretación visual, pero no conservan toda la relación semántica de celdas. En las tablas de layout se requiere revisar el orden de lectura, alineación y texto alternativo durante la conversión futura.
- El artículo Smart Control solo tiene algunas resoluciones preservadas; otras dimensiones y comportamiento con zoom deben validarse en la fase frontend.
- No se consultaron páginas históricas ni se incluyeron tablas fuera de los cinco artículos autorizados.

## Evidencia y referencias

- `docs/33_AUDITORIA_HTML_ARTICULOS.md`: alcance de los 42 artículos, conteos previos y limitaciones del análisis sintáctico.
- `docs/12_PROBLEMAS_RESPONSIVE.md`: antecedente de overflow horizontal en la tabla de 800 px del artículo Moneyball.
- `docs/reference/blog/posts/como-asegurarse-que-los-servicios-de-cloud-computing-sean-ef/desktop-1440x900.png` y `mobile-390x844.png`.
- `docs/reference/blog/posts/smartqa-una-iniciativa-gbit/desktop-1440x900.png` y `mobile-390x844.png`.
- `docs/reference/blog/posts/una-app-para-tu-negocio-considera-una-pwa-entre-tus-opciones/desktop-1440x900.png` y `mobile-390x844.png`.
- `docs/reference/blog/posts/moneyball-el-arte-de-ganar-un-juego-injusto/desktop-1440x900.png` y `mobile-390x844.png`.
- `docs/reference/blog/posts/smart-control-sistema-de-marcacion-y-control-de-esfuerzo/desktop-1440x900.png` y `mobile-390x844.png`.
- Metadatos de estructura de la consulta local `SELECT` restringida a IDs 1080, 1641, 1667, 1669 y 1670; salida temporal sin textos de celdas.
- Código y base ProcessWire originales no fueron modificados. No se inició implementación ni importación.
