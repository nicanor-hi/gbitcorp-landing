# 20 — Validación de codificación del contenido público

## Alcance y método

Comprobación de solo lectura en MySQL portable 8.4.4, `127.0.0.1:3307`, base `processwire_gbitcorp_local`, usuario `pw_auditor`. No se usó `root` ni se contactó producción. Se consultó metadata de `INFORMATION_SCHEMA`, variables de charset de sesión y representaciones `HEX(data)` y `HEX(CONVERT(data USING utf8mb4))` para títulos de las 49 rutas A, 42 `blog_body` y 42 `resume` de artículos A. No se copiaron cuerpos ni bytes al informe.

Las columnas `data` de `field_title`, `field_resume`, `field_blog_body` y `field_blog_images` son `latin1`/`latin1_swedish_ci`. La sesión del cliente usa `utf8mb4` para `character_set_client`, `character_set_connection` y `character_set_results`. La comparación local decodificó los bytes crudos como CP1252 y los cotejó con los bytes UTF-8 producidos por MySQL; en las muestras comparadas coincidieron **49/49 títulos, 42/42 resúmenes y 42/42 cuerpos**.

## Hallazgos confirmados

- En las columnas de texto consultadas, CP1252 reproduce la conversión del propio servidor MySQL a UTF-8. No hubo filas con marcadores comunes de mojibake (`Ã`, `Â`, `â€`) ni caracteres de reemplazo U+FFFD en las muestras.
- Las secuencias de bytes que contienen un signo `?` entre letras corresponden a caracteres `?` literales almacenados en los valores SQL; no las introduce la conversión CP1252 ni el cliente. Se detectaron en 8 cuerpos (778 ocurrencias agregadas) y 7 resúmenes (32 agregadas). En cuerpos con contención exacta, la preservación también muestra este tipo de signos; el cuerpo del artículo 1086 coincide exactamente tras extraer texto, decodificar entidades y normalizar espacios. En otras filas con signos, la comparación normalizada dio alta cobertura de secuencias de ocho palabras, pero no coincidencia textual completa; no quedó verificada individualmente la posición de cada signo en todos los resúmenes.
- El cotejo de texto visible encontró contención exacta para 29/42 cuerpos y mediana de 99,9% de cobertura de shingles de ocho palabras; para resúmenes comparados contra el índice público, la contención exacta fue 0/42 y la mediana de cobertura fue 94,1%. Estos indicadores corroboran relación textual, pero no prueban identidad exacta para todos los valores: el resumen del índice se considera evidencia parcial y requiere revisión editorial antes de importar.
- Los datos crudos de latin1 que también pasan una prueba estricta de UTF-8 (1 cuerpo, 6 resúmenes y 18 títulos) no son por sí mismos indicio de UTF-8 mezclado: el charset de columna confirmado y la coincidencia CP1252→UTF-8 del servidor son la referencia para interpretar esos bytes.
- En la página 1086, el título DB coincide con el título público al colapsar espacios y retirar el sufijo de marca. La diferencia previa era de normalización, no una divergencia editorial demostrada. El H2 visible proviene de `blog_body`; el H4 que imprimía `$page->title` está comentado en el template.
- La decodificación de entidades HTML es independiente de la conversión de charset. El template de artículo ejecuta `html_entity_decode()` en `blog_body`; no debe decodificarse dos veces ni aplicarse globalmente a todo contenido.

## Conclusión y límites

**Codificación de transporte resuelta para las columnas y filas consultadas:** conservar `latin1` de origen y convertir a Unicode/UTF-8 usando la interpretación CP1252 de MySQL. No hay evidencia de doble codificación ni de corrupción introducida al leer estas muestras. Los `?` señalados sí existen literalmente en los datos originales. No es posible inferir qué letra, tilde o carácter pudo haberse querido escribir antes de que ese signo quedara almacenado; no sustituirlo automáticamente. La preservación pública manda, y cualquier corrección editorial debe aprobarse manualmente.

El cotejo normalizado no es identidad byte por byte. No se validó exhaustivamente cada campo HTML de servicios/repetidores ni cada carácter de los 42 cuerpos/resúmenes frente a sus capturas; varios textos no quedaron en contención exacta, aunque su cobertura de shingles fue alta. Los marcadores de mojibake examinados son patrones comunes, no una prueba universal de ausencia de cualquier anomalía.

## Tratamiento futuro en Wagtail

Leer columnas respetando su charset declarado; usar un cliente configurado explícitamente para UTF-8 en el transporte y convertir latin1/CP1252 una sola vez. Aplicar `html_entity_decode` solo a los campos donde lo hace el template y sanitizar HTML con allowlist. Preservar los signos `?` tal como aparecen en la referencia pública durante el primer borrador; marcar el contenido afectado para revisión editorial, sin heurísticas de “reparación”. Añadir pruebas con títulos, tildes, ñ, signos, entidades, los cuerpos/resúmenes identificados y round-trip UTF-8 antes de importar.

No se ejecutaron `ALTER`, `UPDATE`, `REPLACE`, conversiones masivas ni escrituras en MySQL.
