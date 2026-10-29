"""Sube `publicar/` al hosting por FTP, sólo lo que cambió.

Guarda un manifiesto de hashes en `.subida.json`, así la segunda subida
manda 50 KB en vez de 16 MB. Sólo usa la librería estándar.

    ./construir.sh https://cabranegra.mx     # 1. arma
    uv run python subir.py                   # 2. sube lo que cambió
    uv run python subir.py --todo            # fuerza subir todo
    uv run python subir.py --limpiar         # además borra del servidor lo que ya no existe

Credenciales: en `.env` junto a este archivo (está en .gitignore).
Las saca Hostinger de hPanel -> Archivos -> Cuentas FTP.

    FTP_HOST=ftp.tudominio.mx
    FTP_USER=u123456789.cabranegra
    FTP_PASS=...
    FTP_DIR=/public_html
"""
import ftplib
import hashlib
import json
import os
import ssl
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
LOCAL = RAIZ / "publicar"
MANIFIESTO = RAIZ / ".subida.json"
IGNORA = {".DS_Store", "Thumbs.db"}


def carga_env():
    env = RAIZ / ".env"
    if not env.exists():
        sys.exit(
            "Falta el archivo .env junto a subir.py.\n"
            "Créalo con FTP_HOST, FTP_USER, FTP_PASS y FTP_DIR.\n"
            "Los datos salen de hPanel -> Archivos -> Cuentas FTP."
        )
    datos = {}
    for linea in env.read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("#") or "=" not in linea:
            continue
        k, v = linea.split("=", 1)
        datos[k.strip()] = v.strip().strip('"').strip("'")
    faltan = [k for k in ("FTP_HOST", "FTP_USER", "FTP_PASS") if not datos.get(k)]
    if faltan:
        sys.exit(f"Al .env le faltan: {', '.join(faltan)}")
    datos.setdefault("FTP_DIR", "/public_html")
    return datos


def huella(p: Path) -> str:
    h = hashlib.md5()
    with p.open("rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def archivos_locales():
    """Ruta relativa (con / como separador) -> hash."""
    fuera = {}
    for p in sorted(LOCAL.rglob("*")):
        if p.is_dir() or p.name in IGNORA:
            continue
        fuera[p.relative_to(LOCAL).as_posix()] = huella(p)
    return fuera


def conecta(cfg):
    """Intenta FTPS; si el servidor no lo soporta, cae a FTP simple."""
    try:
        ftp = ftplib.FTP_TLS(cfg["FTP_HOST"], timeout=40,
                             context=ssl.create_default_context())
        ftp.login(cfg["FTP_USER"], cfg["FTP_PASS"])
        ftp.prot_p()
        print("conectado por FTPS (cifrado)")
    except (ftplib.error_perm, ssl.SSLError, OSError):
        ftp = ftplib.FTP(cfg["FTP_HOST"], timeout=40)
        ftp.login(cfg["FTP_USER"], cfg["FTP_PASS"])
        print("conectado por FTP simple — el servidor no ofreció cifrado")
    ftp.set_pasv(True)
    ftp.cwd(cfg["FTP_DIR"])
    return ftp


def asegura_dir(ftp, base, rel):
    """Crea los directorios intermedios de una ruta relativa."""
    partes = rel.split("/")[:-1]
    ruta = base
    for parte in partes:
        ruta = f"{ruta}/{parte}"
        try:
            ftp.mkd(ruta)
        except ftplib.error_perm as e:
            if not str(e).startswith("550"):   # 550 = ya existe
                raise


def main():
    todo = "--todo" in sys.argv
    limpiar = "--limpiar" in sys.argv

    if not LOCAL.is_dir():
        sys.exit("No existe publicar/. Corre primero ./construir.sh")

    cfg = carga_env()
    ahora = archivos_locales()
    antes = {} if todo else json.loads(
        MANIFIESTO.read_text()) if MANIFIESTO.exists() else {}

    nuevos = [r for r, h in ahora.items() if antes.get(r) != h]
    sobran = [r for r in antes if r not in ahora]

    if not nuevos and not (limpiar and sobran):
        print("nada cambió — no hay qué subir")
        return

    peso = sum((LOCAL / r).stat().st_size for r in nuevos)
    print(f"por subir: {len(nuevos)} archivo(s), {peso/1024/1024:.1f} MB")

    ftp = conecta(cfg)
    base = cfg["FTP_DIR"].rstrip("/")
    subidos = 0
    try:
        for rel in nuevos:
            asegura_dir(ftp, base, rel)
            with (LOCAL / rel).open("rb") as f:
                ftp.storbinary(f"STOR {base}/{rel}", f, blocksize=1 << 18)
            subidos += 1
            print(f"  [{subidos}/{len(nuevos)}] {rel}")
            antes[rel] = ahora[rel]

        if limpiar:
            for rel in sobran:
                try:
                    ftp.delete(f"{base}/{rel}")
                    print(f"  borrado {rel}")
                    antes.pop(rel, None)
                except ftplib.error_perm as e:
                    print(f"  no se pudo borrar {rel}: {e}")
    finally:
        # guarda lo que sí alcanzó a subir, aunque se caiga a medias
        MANIFIESTO.write_text(json.dumps(antes, indent=1, sort_keys=True))
        try:
            ftp.quit()
        except Exception:
            ftp.close()

    print(f"listo — {subidos} archivo(s) en el servidor")
    if any(r.endswith(".html") for r in nuevos):
        print("tip: recarga con Cmd+Shift+R, el navegador guarda el HTML viejo un rato")


if __name__ == "__main__":
    main()
