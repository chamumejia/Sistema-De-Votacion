import json
from datetime import datetime
from pathlib import Path

from actividad import registrar_actividad


CANDIDATOS = {
    "Ana": 0,
    "Carlos": 0,
    "Luisa": 0
}

ARCHIVO_VOTOS = Path("votos.txt")
HISTORIAL = Path("historial_votacion.txt")


def cargar_votos():
    if not ARCHIVO_VOTOS.exists():
        return {
            "candidatos": CANDIDATOS.copy(),
            "votantes": {}
        }

    try:
        with ARCHIVO_VOTOS.open("r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except (json.JSONDecodeError, OSError):
        return {
            "candidatos": CANDIDATOS.copy(),
            "votantes": {}
        }


def guardar_votos(datos):
    with ARCHIVO_VOTOS.open("w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)


def registrar_voto(
    nombre,
    apellidos,
    tipo_documento,
    numero_documento,
    candidato
):
    nombre = nombre.strip()
    apellidos = apellidos.strip()
    tipo_documento = tipo_documento.strip().upper()
    numero_documento = numero_documento.strip()
    candidato = candidato.strip()

    if not all([
        nombre,
        apellidos,
        tipo_documento,
        numero_documento,
        candidato
    ]):
        registrar_actividad("Voto rechazado: faltan datos")
        return False, "Todos los campos son obligatorios."

    datos = cargar_votos()
    candidatos = datos["candidatos"]
    votantes = datos["votantes"]

    documento = f"{tipo_documento}:{numero_documento}"

    if candidato not in candidatos:
        registrar_actividad("Voto rechazado: candidato inválido")
        return False, "El candidato seleccionado no existe."

    if documento in votantes:
        registrar_actividad(
            f"Voto duplicado rechazado: {documento}"
        )
        return False, "Esta persona ya realizó su voto."

    votantes[documento] = {
        "nombre": nombre,
        "apellidos": apellidos,
        "tipo_documento": tipo_documento,
        "numero_documento": numero_documento,
        "candidato": candidato,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    candidatos[candidato] += 1
    guardar_votos(datos)

    registrar_actividad(
        f"Voto registrado: {documento} eligió a {candidato}"
    )

    return True, f"Voto registrado correctamente para {candidato}."


def ver_resultados():
    datos = cargar_votos()
    candidatos = datos["candidatos"]
    total = sum(candidatos.values())
    resultados = []

    for candidato, cantidad in candidatos.items():
        porcentaje = 0

        if total > 0:
            porcentaje = cantidad / total * 100

        resultados.append({
            "nombre": candidato,
            "votos": cantidad,
            "porcentaje": round(porcentaje, 2)
        })

    registrar_actividad("Resultados consultados")

    return resultados, total


def reiniciar_votacion():
    datos = cargar_votos()
    resultados, total = ver_resultados()

    with HISTORIAL.open("a", encoding="utf-8") as archivo:
        archivo.write(
            f"\n--- Reinicio: "
            f"{datetime.now():%Y-%m-%d %H:%M:%S} ---\n"
        )
        archivo.write(f"Total de votos: {total}\n")

        for resultado in resultados:
            archivo.write(
                f"{resultado['nombre']}: "
                f"{resultado['votos']} votos "
                f"({resultado['porcentaje']}%)\n"
            )

    datos["candidatos"] = CANDIDATOS.copy()
    datos["votantes"] = {}

    guardar_votos(datos)
    registrar_actividad("Votación reiniciada")

    return True
