# Contexto del proyecto gbitcorp-landing

## Objetivo

Migrar el sitio corporativo público `https://gbitcorp.com` de ProcessWire a Django + Wagtail y PostgreSQL. La prioridad es reconstruir con alta fidelidad lo comprobado públicamente y en los archivos locales, con mejor comportamiento responsive y administración de contenido en Wagtail.

## Estado de fase

Fases 0, 0.1 y revisión específica del Home (auditoría, preparación y preservación pública) completadas. No se ha creado código Django/Wagtail ni instalado ninguna dependencia del producto. La siguiente fase requiere aprobación del usuario.

## Hechos observados

- Respaldo local en `docs/gbitcorp.com/`, excluido de Git. El core declara ProcessWire **3.0.229** (`wire/core/ProcessWire.php`).
- El respaldo contiene `wire/` (core), `site/templates/`, `site/modules/` y `site/assets/`; el conteo local fue de 3,786 archivos.
- `site/templates/` tiene 44 archivos PHP y recursos CSS, JS, imágenes, SVG, iconos y fuentes. Hay carpetas `old` y `old2` que necesitan revisión de uso antes de migrar.
- Se contaron 728 archivos en `site/assets/files/`. FASE 0.6.1 concilió `blog_images`: 74 referencias en 42 artículos + 1 en el índice público `/blog/posts/` (ID 1037, archivo `1144-1.jpg`, usado como fondo del encabezado) = 75 medios `blog_images` A locales. La tabla tiene 76 filas; una queda fuera del manifiesto público. Sumadas 83 referencias `icon` y 14 `image`, hay 172 referencias de medios A locales; esto no mapea ni aprueba todo el directorio.
- Se observaron módulos locales de formularios, blog, suscripción, programación de páginas, correo SMTP y compartición social, junto con módulos de terceros. Ver `docs/01_AUDITORIA_PROCESSWIRE.md`.
- Se preservaron 49 páginas públicas HTTP 200 a través de 51 destinos internos únicos intentados; dos variantes `www.gbitcorp.com` fallaron antes de navegación por error de certificado. En las páginas se encontraron 1,645 apariciones de enlaces: 992 internos, 414 externos y 239 especiales. No se navegó a destinos externos. `robots.txt` y `sitemap.xml` devolvieron 404.
- `docs/reference/` contiene 351 PNG (49 páginas × 7 viewports y 8 capturas de interacción), junto a texto visible completo, metadatos/estructura por página, manifest, CSV de enlaces, recursos y mediciones responsive. Resoluciones: 1920×1080, 1440×900, 1366×768, 1024×768, 768×1024, 390×844 y 375×812. La cobertura y excepciones se detallan en `docs/07_PRESERVACION_SITIO.md`.
- Mediciones de scroll horizontal: 0/49 páginas en 1920, 1440 y 1366; 3/49 a 1024; 10/49 a 768; 18/49 a 390 y 375. Hay casos de imágenes/tablas de ancho fijo y contenido editorial desbordado; ver `docs/12_PROBLEMAS_RESPONSIVE.md`.
- En auditoría puntual adicional del Home, las vueltas dieron `loadEventEnd` terminado de 12.8–18.3 s (una captura móvil quedó todavía pendiente) frente a HTML recibido en 0.59–0.65 s, en headless sin throttling; mobile `DOMContentLoaded` + 1.2 s mostró el fondo del hero aún sin pintar. Se guardaron capturas inicial/completa en desktop/tablet/móvil y telemetría sin query strings en `docs/reference/home/`; ver `docs/14_DIAGNOSTICO_HOME_RENDIMIENTO.md`. El fondo de ciudad pesa 5.05 MB; hay fondos `cover` de proporciones muy distintas a las secciones y fotografías/carrusel de 1.5–2.1 MB. Causa/tiempos por recurso pueden variar por red y servicios terceros.
- La inspección visual nueva detectó espacio vertical excesivo bajo las tarjetas del blog en tablet/móvil; `.blog` conserva altura fija de 1440 px en CSS móvil. El detalle y el estado completo están en el diagnóstico Home.
- La portada incluye un formulario que envía a Zoho CRM; no se envió. Su destino y campos deben revisarse funcionalmente antes de reconstruir.
- Se restauró localmente el dump autorizado en `processwire_gbitcorp_local`, en MySQL portable `127.0.0.1:3307`. Auditoría read-only confirmó servidor 8.4.4; el encabezado del dump declara origen MariaDB 10.11.16. No conectarse a RDS ni repetir dump/restauración. La copia contiene datos potencialmente sensibles; no consultar ni migrar valores de usuarios, hashes, sesiones, comentarios o formularios.
- Esquema confirmado: 80 tablas (68 `field_*`), 762 páginas, 53 templates, 67 fields, 56 fieldgroups y 174 asociaciones fieldgroup-field. Todas InnoDB y collation `latin1_swedish_ci`, frente al default utf8mb4 de base; no hay FK declaradas. Las 49 rutas públicas HTTP 200 tienen match exacto en la base. Ver `docs/15_`–`docs/19_`.
- **Prioridad de contenido:** las 49 rutas preservadas en el sitio público fijan el alcance. MySQL solo complementa sus campos/relaciones/assets; no habilita importar páginas históricas o registros adicionales. `pw_auditor@127.0.0.1` tiene `SELECT, SHOW VIEW` solo sobre la base local; no se usó `root` ni RDS. Las 49 rutas tienen match de ID, jerarquía y template en SQL. Los 48 títulos cuyo template consume el título DB coinciden con la referencia pública tras normalizar espacios/sufijo de marca; la página 1086 usa `blog_body` para el H2 visible y su H4 `$page->title` está comentado. EULA toma texto de `eula.php` estático.
- Charset confirmado: `field_title.data`, `field_resume.data`, `field_blog_body.data` son `latin1`; la sesión es `utf8mb4`. La decodificación CP1252 coincide con la conversión MySQL a UTF-8 en 49/49 títulos, 42/42 resúmenes y 42/42 cuerpos. No hubo marcadores comunes de mojibake ni U+FFFD. Se detectaron signos `?` literales almacenados (8 cuerpos, 7 resúmenes), también visibles en contenido preservado; no intentar restaurar letras por heurística. Algunos resúmenes no tuvieron coincidencia exacta de extracción y requieren revisión editorial; ver `docs/20_`.
- Dependencias B confirmadas: 10 repetidores de Home, 19 elementos `content` y 64 `tools` en las cuatro páginas de servicio, cinco categorías relacionadas y visibles en filtros, y 172 referencias de medios (75 `blog_images`, 83 `icon`, 14 `image`), todas con coincidencia local. Los 191 targets únicos de tags no se ven en los templates públicos inspeccionados y quedan C/excluidos; también se excluyen nueve servicios adicionales no preservados.
- La auditoría consultó solo páginas A y dependencias necesarias; no se consultaron valores sensibles ni campos privados. La cuenta tiene permisos de lectura de esquema, por lo que sigue siendo obligatoria la disciplina de consultas acotadas.

## Entorno y dependencias

- Windows y PowerShell.
- Python del proyecto gestionado por uv: **CPython 3.13.17**, fijado en `.python-version`. Intérprete administrado: `%APPDATA%\uv\python\cpython-3.13.17-windows-x86_64-none\python.exe`. `uv` **0.13.5** está instalado en `%USERPROFILE%\.local\bin` mediante el instalador oficial de Astral.
- `.venv/` fue recreado con `uv venv --clear --python 3.13.17 --managed-python .venv`; `pyvenv.cfg` apunta a la distribución uv, `sys.prefix != sys.base_prefix` y no hay paquetes de aplicación instalados. `.venv/` sigue excluido de Git.
- Python global de Windows permanece intacto e independiente: `C:\Users\nican\AppData\Local\Programs\Python\Python310\python.exe`, versión 3.10.5. El comando global `python` sigue resolviendo a esa instalación; no se añadió Python 3.13 al PATH ni se cambió el ejecutable global.
- Playwright global 1.61.1 por Volta con Chromium 1228. El documento local fue leído íntegramente y sus instrucciones respetadas.
- Aún deben seleccionarse versiones compatibles de Django/Wagtail antes de instalar dependencias. No se instaló Django ni Wagtail en este ajuste.

## Arquitectura objetivo (propuesta, no implementada)

- Django con PostgreSQL y Wagtail para edición.
- Modelos de página basados en tipos reales encontrados: portada, páginas de servicios/negocio, listados y artículos del blog, páginas informativas y licencia/EULA si continúa vigente.
- StreamField para secciones de composición variable y editables; definir bloques después de revisar todas las plantillas y páginas verificadas.
- Imágenes y documentos administrados por Wagtail. Snippets/settings para navegación, footer y datos corporativos compartidos si el modelo de contenido lo confirma.
- Formularios implementados con validación, protección contra abuso, almacenamiento mínimo y destino de integración explícito; no trasladar configuración SMTP/Zoho antigua ni secretos.
- Mapa de URL con conservación de slugs y redirecciones 301 solo cuando sean necesarias y verificadas.

## Decisiones y límites

- No usar ni modificar el proyecto original; no versionar el respaldo ProcessWire ni el documento fuente de Playwright.
- No instalar dependencias Django/Wagtail en Fase 0.
- Las páginas protegidas, no enlazadas, privadas o dependientes de datos MySQL no se inventan ni se publican automáticamente.
- La preservación pública es la fuente principal del alcance migrable; la base ProcessWire es complementaria y no autoriza ampliar el contenido.
- Las mejoras responsive pueden reemplazar divisores de imagen por CSS/SVG responsive, preservando intención visual.
- Ver la auditoría inicial en `docs/01_AUDITORIA_PROCESSWIRE.md` a `docs/06_PLAN_MIGRACION.md`, preservación en `docs/07_PRESERVACION_SITIO.md` a `docs/14_DIAGNOSTICO_HOME_RENDIMIENTO.md`, y auditoría/modelo/mapeo DB en `docs/15_AUDITORIA_MYSQL_PROCESSWIRE.md` a `docs/19_ESTRATEGIA_IMPORTACION.md`.
- FASE 0.5–0.6.1 documenta codificación, manifiesto de 49 rutas, clasificación editorial, assets, preparación del importador y cierre en `docs/20_` a `docs/25_`; el CSV `docs/21_MANIFIESTO_CONTENIDO_VIGENTE.csv` sigue siendo una allowlist candidata, no aprobación de publicación.
- El respaldo ProcessWire y el documento fuente Playwright permanecen locales e ignorados. Las referencias de assets apuntan a las rutas del respaldo; no se copiaron assets binarios a `docs/reference/`, por lo que estas referencias no son autosuficientes si se pierde el respaldo local. No se modificó el original.
