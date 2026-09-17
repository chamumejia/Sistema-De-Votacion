from datetime import datetime
from pathlib import Path


ARCHIVO_ACTIVIDAD = Path("actividad.txt")


def registrar_actividad(mensaje):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with ARCHIVO_ACTIVIDAD.open("a", encoding="utf-8") as archivo:
        archivo.write(f"[{fecha}] {mensaje}\n")
    