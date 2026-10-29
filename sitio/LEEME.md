# Sitio Cabra Negra

## La regla
El fuente es **`index.html`**. `publicar/` es **generado** — `construir.sh`
la borra y la rehace. Nunca edites ahí ni en el administrador de archivos
del hosting: el siguiente build se lo lleva.

```
index.html  ──construir.sh──>  publicar/  ──subir.py──>  hosting
 (editas)                      (generado)                 (vivo)
```

## Editar y volver a publicar
```bash
# 1. editas index.html
./construir.sh https://cabranegra.mx
uv run python subir.py
```
`subir.py` compara hashes y sube sólo lo que cambió: un cambio de texto son
~50 KB, no los 16 MB completos.

## Dónde está cada cosa en index.html
| Qué quieres cambiar | Dónde |
|---|---|
| Número de WhatsApp | constante `WHATSAPP` al inicio del `<script>` |
| Productos del catálogo y del carrusel | arreglo `PRODUCTOS` |
| Logos de clientes | arreglo `CLIENTES` |
| Textos de la portada | bloques `.titular` y `.intro` |
| Los dos paneles del scroll | `.panel-madera` y `.panel-grabado` |
| Colores de marca | bloque `:root` del `<style>` |
| Momentos de la animación | función `actualiza()`, los `tramo(...)` |

## Cambiar una foto
Deja el mismo nombre de archivo en `assets/img/` y vuelve a correr los dos
comandos. Si le pones otro nombre, actualiza también la referencia en
`index.html`.

## El video de portada
Se genera aparte con ffmpeg a partir de las fotos del catálogo. El
procedimiento quedó anotado en la memoria del proyecto. Dura 12.6 s y va
codificado con todos los fotogramas clave para que rebobine parejo.

## Cuidado
- `.env` trae la contraseña del FTP y **no se versiona**.
- Después de subir HTML, recarga con `Cmd+Shift+R`.
