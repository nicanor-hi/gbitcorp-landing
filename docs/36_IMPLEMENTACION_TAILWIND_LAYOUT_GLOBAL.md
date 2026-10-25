# 36 — Integración Tailwind CSS y layout global

**Estado:** FASE 2.2B implementada. Esta fase entrega infraestructura compartida; no implementa las páginas completas ni importa contenido.

## Dependencias y ejecución

- Node.js `v22.13.0`, seleccionado por Volta.
- npm `10.9.2` fue reportado como verificado funcional en el diagnóstico previo. En la comprobación de esta sesión, `volta run --node 22.13.0 npm --version` devolvió `10.9.0`; queda registrada la diferencia, sin atribuirla a una instalación dañada ni modificar herramientas.
- `tailwindcss` y `@tailwindcss/cli` fijados en `4.3.3`; `package-lock.json` fija el árbol transitivo.
- La instalación `npm ci` y el build se ejecutan con Volta. En este PowerShell el launcher `npm.ps1` puede resolver incorrectamente rutas internas de npm; no se debe usar el comando desnudo `npm` ni cambiar la instalación global. `npm.cmd` funciona como alternativa verificada, pero los comandos documentados y reproducibles del proyecto son:

  ```powershell
  volta run --node 22.13.0 npm ci
  volta run --node 22.13.0 npm run dev
  volta run --node 22.13.0 npm run css:watch
  volta run --node 22.13.0 npm run build
  ```

  El diagnóstico de Volta/npm se limita a la resolución del shim de PowerShell: `volta run --node 22.13.0 npm --version` ejecuta npm correctamente. Volta, Node y npm no se reinstalaron ni modificaron.

## Archivos y compilación

- `package.json`, `package-lock.json`: CLI local, versiones exactas y scripts.
- `static/src/css/site.css`: entrada Tailwind v4, tokens y reglas base.
- `static/css/site.css`: salida compilada, generada localmente e ignorada por Git.
- `static/js/site-navigation.js`: mejora progresiva del menú móvil.
- `static/images/brand/logo-gbit.png`: única imagen original copiada; logo público visible del header, procedente de `site/templates/img/new/Logo Completo GBIT .png`. El original permanece intacto.
- `templates/base.html`, `templates/includes/header.html`, `templates/includes/footer.html`: estructura global reutilizable.
- `config/context_processors.py`: enlaces observados y consulta de solo lectura de `SiteFooterSettings`; no crea settings al renderizar.
- `editorial/tests/test_global_layout.py`: pruebas con la base efímera del test runner.

Tailwind importa su CSS desde `static/src/css/site.css` y limita el escaneo a `templates/` y `static/js/`. No escanea ProcessWire, documentación, capturas, contenido de base de datos ni `node_modules`. Las clases deben permanecer completas y estáticas. Django sirve el CSS generado mediante staticfiles; Node no participa en las peticiones HTTP. No se configuró un CDN.

## Tokens y alcance visual

Los colores de marca, Noto Sans como familia declarada, y la sombra de navegación proceden de valores observados en el CSS original y están centralizados en `@theme`. La fuente Noto Sans no se distribuyó: la auditoría original no confirmó su carga efectiva/licencia; hay fallback a Arial/sans-serif y la equivalencia tipográfica queda pendiente.

Los breakpoints `md` (48rem), `lg` (64.0625rem) y `xl` (85.4375rem) reproducen los cortes originales medidos en píxeles convertidos a rem; son valores de implementación inferidos de las reglas legacy, no una medición visual validada del layout nuevo. Foco visible y `prefers-reduced-motion` se implementan como reglas base.

El header usa fondo blanco opaco y sticky para legibilidad. En Home el original presenta tratamiento transparente/superpuesto; esta diferencia se deja explícita para la fase de implementación del Home, donde podrá agregarse una variante respaldada por capturas. Los enlaces de navegación corresponden a anclas públicas verificadas, pero esta fase no implementa las secciones que las recibirán.

## Comportamiento compartido

- `base.html`: idioma español, metadata básica disponible, skip link, landmarks `header/main/footer`, CSS, JS modular y bloques para páginas futuras.
- Header desktop/móvil: logo, enlaces confirmados y botón accesible con `aria-expanded`, `aria-controls` y etiqueta actualizada. Sin JS la navegación permanece visible; el script la oculta inicialmente en viewport móvil, gestiona Escape, cierre al seguir enlace, foco al cerrar mediante Escape y cambios de viewport.
- Footer: renderiza únicamente los valores presentes en `SiteFooterSettings` (contacto y enlaces sociales). La lectura es de solo lectura y el estado vacío no crea registros. Se muestran enlaces globales documentados; no se inventan datos de contacto.
- EULA es autónoma en el contrato de páginas y no se debe asumir que usará este footer/header; esta fase deja la base disponible para que sus templates futuros decidan según la evidencia.

## Validación y límites

La suite `editorial.tests.test_global_layout` cubre landmarks/assets, rutas estructurales que no deben enlazarse, footer vacío sin escrituras y valores configurados. El test runner usa su base temporal; no se crearon páginas ni settings en la base permanente. El build de Tailwind produce CSS minificado.

Esta fase no incluye vistas ni templates completos de Home, blog, servicios o EULA; no incluye carruseles, formularios Zoho, importación de medios, ni comparación visual Playwright del frontend nuevo. Solo se incorporó el logo del header confirmado. No se generaron ni copiaron otros assets.

Pendientes de FASE 2.3: implementar Home con sus campos y bloques aprobados; definir la variante visual del header sobre el hero; comparar con las capturas preservadas en los viewports acordados; confirmar fuente/licencia; validar enlaces de ancla con las secciones renderizadas y ajustar cualquier diferencia visual significativa con evidencia. Las 49 rutas siguen sin contenido importado y `import_authorized=No`.
