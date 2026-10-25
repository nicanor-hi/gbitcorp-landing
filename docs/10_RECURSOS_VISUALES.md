# 10 — Recursos visuales

Para la lista de recursos de Home que dominan la carga, dimensiones/peso de fondos, comportamiento `cover`, galerías/carruseles y plan de optimización de renditions en Wagtail, ver [14_DIAGNOSTICO_HOME_RENDIMIENTO.md](14_DIAGNOSTICO_HOME_RENDIMIENTO.md#secciones-imágenes-de-fondo-y-separadores).

El manifiesto y cada `page.json` conservan las imágenes `<img>`, alt, dimensiones observadas, fondos CSS, hojas de estilo y scripts usados por las páginas. El inventario por aparición está en [assets.csv](reference/assets.csv).

- Apariciones de imágenes/fondos mapeadas: 933.
- Recursos únicos (URL + tipo): 239.
- Referencias con archivo coincidente en el respaldo local: 226.
- Capturas de preservación: 351.

Las rutas originales se guardan relativas a `docs/gbitcorp.com/`, sin copiar ni alterar el respaldo. Los recursos externos enlazados no se descargaron; las URLs de recursos externos cargados por las páginas se guardan sin query strings.

| Tipo de recurso | Apariciones |
|---|---:|
| image | 877 |
| section background | 14 |
| background: header .intro.introhalf | 42 |

Las imágenes de `site/assets/files/` dependen de IDs y asociaciones de MySQL. El CSV identifica los archivos que existen en el respaldo, pero su asociación editorial debe confirmarse. Recursos no mapeados requieren revisión manual; no son prueba de que el archivo esté roto.
