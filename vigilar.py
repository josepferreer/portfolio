"""Vigilante: regenera el portfolio solo, sin tener que ejecutar generar.py a mano.

Uso: python vigilar.py   (o doble clic en vigilar.bat). Se para cerrando la ventana o con Ctrl+C.

Mira cada 2 segundos:
  - img/archivo/          (soltar, cambiar o borrar imágenes sueltas)
  - proyectos.json
  - plantillas/portada.html
Cuando algo cambia, espera a que el archivo termine de copiarse y ejecuta generar.py.
Solo regenera la web en este ordenador: NO sube nada a GitHub.
"""
import subprocess
import sys
import time
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
ARCHIVO = RAIZ / "img" / "archivo"
SUELTOS = [RAIZ / "proyectos.json", RAIZ / "plantillas" / "portada.html"]
FORMATOS = {".png", ".jpg", ".jpeg", ".webp"}


def _slug(texto):
    """La misma regla de nombres que usa generar.py para las copias de img/archivo/web/."""
    import re
    import unicodedata
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-") or "imagen"


def estado():
    """Huella de lo vigilado: nombre, tamaño y fecha de cada archivo."""
    h = {}
    if ARCHIVO.is_dir():
        for f in ARCHIVO.iterdir():
            if f.is_file() and f.suffix.lower() in FORMATOS:
                s = f.stat()
                h[f.name] = (s.st_size, s.st_mtime)
    for f in SUELTOS:
        if f.exists():
            s = f.stat()
            h[str(f)] = (s.st_size, s.st_mtime)
    return h


def limpiar_copias():
    """Si borras una imagen de img/archivo/, quita también su copia de img/archivo/web/."""
    web = ARCHIVO / "web"
    if not web.is_dir():
        return
    vivas = {_slug(f.stem) + ".jpg" for f in ARCHIVO.iterdir() if f.is_file() and f.suffix.lower() in FORMATOS}
    for c in web.glob("*.jpg"):
        if c.name not in vivas:
            c.unlink()
            print(f"  quitada la copia {c.name} (ya no está el original)")


def generar():
    hora = time.strftime("%H:%M:%S")
    print(f"[{hora}] cambios: generando…")
    limpiar_copias()
    r = subprocess.run([sys.executable, "-I", str(RAIZ / "generar.py")], cwd=RAIZ, capture_output=True, text=True)
    salida = (r.stdout + r.stderr).strip()
    print("  " + salida.replace("\n", "\n  ") if salida else "  hecho")


if __name__ == "__main__":
    print("Vigilando img/archivo/, proyectos.json y la portada. Cierra esta ventana para parar.")
    antes = estado()
    generar()
    while True:
        time.sleep(2)
        ahora = estado()
        if ahora == antes:
            continue
        # espera a que la copia termine: dos lecturas seguidas iguales
        while True:
            time.sleep(1.5)
            otra = estado()
            if otra == ahora:
                break
            ahora = otra
        antes = ahora
        generar()
