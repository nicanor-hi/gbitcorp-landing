# FASE 1.2C — Validación editorial y administrativa Wagtail

## 1. Alcance y método

Se validó la estructura editorial vacía implementada en FASE 1.2B con Django 5.2.18, Wagtail 7.4.4, Python 3.13.17 y PostgreSQL 16.1. Las fixtures editoriales y el usuario administrativo se crearon exclusivamente en la base temporal que genera el test runner de Django, y se eliminaron al terminar. No se cargó contenido en la base de desarrollo ni se consultó MySQL/ProcessWire.

La cobertura se añadió en `editorial/tests/test_editorial_models.py` y `editorial/tests/test_streamfield_contract.py`. Se probaron los modelos, el registro Wagtail, los formularios de administración con cliente Django, las reglas del árbol, la resolución del manifiesto y la serialización de bloques.

## 2. Modelos y administración

Se comprobaron `HomePage`, `BlogIndexPage`, `BlogPostPage`, `ServicePage`, `EulaPage`, `RouteContainerPage`, el snippet `BlogCategory` y `SiteFooterSettings`.

- Los cinco tipos editoriales y el contenedor estructural tienen handlers de edición con paneles.
- `BlogCategory` está registrado como snippet; `SiteFooterSettings`, en el registro de settings de Wagtail.
- La petición anónima a administración de páginas, snippet y settings se redirige a autenticación (302). Con un superusuario efímero de la base de pruebas, `/admin/`, el listado de categorías y los editores de página/settings responden 200; se confirmó que el selector de categorías y los campos del footer se muestran.
- El usuario de prueba no se creó en la base PostgreSQL permanente y no se configuró ninguna credencial permanente.

## 3. Jerarquía y URLs

La prueba lee `docs/21_MANIFIESTO_CONTENIDO_VIGENTE.csv`: verifica 49 rutas únicas y construye una jerarquía temporal de 56 nodos (49 públicos, incluida la raíz, más siete ancestros estructurales). Las 49 rutas resuelven con `Page.route_for_request` al tipo editorial correspondiente y conservan sus segmentos de ruta. Cada una de las siete rutas estructurales devuelve 404 en el cliente Django y está fuera de menús, búsqueda y sitemap. No se creó ninguna página en la base de desarrollo.

La prueba verifica resolución de ruta Wagtail, no renderizado de páginas: todavía no existe frontend público ni se afirma paridad visual/HTTP 200 para páginas editoriales.

## 4. StreamField, medios y relaciones

- `HomePage.sections` solo admite los seis bloques aprobados por el contrato; un bloque de texto sin encabezado requerido falla validación.
- `BlogPostPage.body` admite únicamente el bloque `rich_text` con las features restringidas documentadas. La serialización/deserialización conserva orden y valores. No existe bloque `raw_html`.
- `ServicePage.content_blocks` conserva su estructura repetible tipada y rechaza un offering sin título; `tools` limita tipos al bloque de imagen aprobado.
- EULA conserva el allowlist de formato de RichText del contrato.
- Se guardó una imagen PNG temporal fuera del repositorio, se relacionó con artículo y StreamField, y se comprobó el round-trip del bloque y la nulabilidad de la relación al borrar el medio (`SET_NULL`). El directorio temporal se limpia automáticamente.
- En el flujo Wagtail, la relación M2M de categorías se probó tras guardar y publicar una revisión temporal. Se confirmó que el `add()` repetido no duplica asociaciones, que caben varias categorías, y que al eliminar una categoría desaparece su asociación sin eliminar el artículo.

## 5. Seguridad y configuración

- `config.settings.local` carga con `DEBUG=True`, host local y backend PostgreSQL.
- `config.settings.production` pudo importarse con variables ficticias de validación en un proceso aislado: `DEBUG=False`, redirect HTTPS, cookies seguras y cabecera de proxy presentes. No se accedió a una base productiva. No se cambió HSTS.
- Las pruebas confirman que las features de RichText están restringidas y que no hay bloque de HTML libre en el contrato implementado. Esto no sustituye la sanitización/validación que deberá realizar el futuro importador del HTML ProcessWire: todavía no existe conversor, staging ni integración Zoho activa.
- El esquema continúa usando exclusivamente `DATABASE_URL`; esta validación no leyó ni mostró `.env`.
- Revisión de código: no se hallaron endpoints ni llamadas a Zoho en configuración o app editorial. No se probaron envíos externos.

## 6. Validaciones técnicas

| Comando / comprobación | Resultado |
|---|---|
| `uv run python manage.py test` | OK — 16 tests |
| `uv run python manage.py check` | OK — 0 issues |
| `uv run python manage.py makemigrations --check --dry-run` | OK — no changes detected |
| `uv run python manage.py migrate --check` | OK |
| `git diff --check` | OK; solo avisos de conversión LF/CRLF en archivos preexistentes |
| Base de desarrollo `gbitcorp_wagtail_dev` | Conexión local; 0 HomePage, 0 BlogCategory y 0 SiteFooterSettings; sin contenido editorial sembrado |

No se generaron ni aplicaron migraciones durante esta fase. La migración editorial existente permanece al día.

## 7. Hallazgos y correcciones

Una prueba inicial de M2M consultaba relaciones antes de persistir la revisión de la página. Se corrigió para seguir el flujo editorial real de Wagtail (`save_revision().publish()`), volver a consultar la página y verificar el borrado de la asociación. No era un defecto del modelo y no requirió cambios de esquema.

No se encontró discrepancia de modelos que justificara alterar campos, relaciones o migraciones.

## 8. Límites y riesgos pendientes

- La validación de las 49 rutas prueba el enrutamiento Wagtail y las siete respuestas 404 en fixtures; no prueba aún HTML público, templates ni diseño.
- No se incorporó ni revisó contenido real, categorías, assets, formulario Zoho ni EULA.
- RichText con features restringidas reduce superficie, pero no es una garantía de sanitización del HTML fuente. El futuro importador deberá validar/transformar mediante allowlist, rechazar estructuras no soportadas y someterlas a revisión; no debe pasar HTML heredado directamente a renderizado.
- Los controles de producción se importaron con entorno ficticio, no validan reverse proxy, TLS, hosts ni secretos del despliegue real.
- Las pruebas cubren administración mediante cliente Django, no una sesión interactiva del navegador ni una cuenta permanente.

## 9. Estado y siguiente paso

FASE 1.2C queda validada para la estructura editorial vacía. No se autoriza por este resultado la importación/publicación de contenido ni la construcción del frontend. El siguiente trabajo puede proponerse por separado: FASE 1.3 para implementación frontend únicamente después de aprobación de alcance, o una fase controlada de definición/importación editorial cuando se apruebe explícitamente. Las 49 rutas siguen con `import_authorized=No`.
