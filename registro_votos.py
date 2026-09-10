# registro_votos.py

# Candidatos disponibles
votos = {
    "Candidato 1": 0,
    "Candidato 2": 0,
    "Candidato 3": 0
}

# Diccionario que guarda los votantes registrados
# La clave será el tipo y número de documento
votantes = {}


def registrar_voto(nombre, apellidos, tipo_documento, numero_documento, candidato):
    """
    Registra el voto de una persona.
    No permite votar dos veces con el mismo documento.
    """

    nombre = nombre.strip()
    apellidos = apellidos.strip()
    tipo_documento = tipo_documento.strip().upper()
    numero_documento = numero_documento.strip()
    candidato = candidato.strip()

    # Validar que los datos personales estén completos
    if not nombre or not apellidos:
        return "Error: el nombre y los apellidos son obligatorios."

    if not tipo_documento or not numero_documento:
        return "Error: el tipo y número de documento son obligatorios."

    # Validar que el candidato exista
    if candidato not in votos:
        return "Error: el candidato no existe."

    # Crear una identificación única con el documento
    identificacion = (tipo_documento, numero_documento)

    # Verificar si la persona ya votó
    if identificacion in votantes:
        return "Error: esta persona ya realizó su voto."

    # Guardar la información del votante
    votantes[identificacion] = {
        "nombre": nombre,
        "apellidos": apellidos,
        "tipo_documento": tipo_documento,
        "numero_documento": numero_documento,
        "candidato": candidato
    }

    # Aumentar el conteo del candidato
    votos[candidato] += 1

    return f"Voto registrado correctamente para {candidato}."


def iniciar_votacion():
    """
    Solicita los datos del votante desde la consola.
    """

    print("===== SISTEMA DE VOTACIÓN =====")
    print()

    nombre = input("Ingrese su nombre: ")
    apellidos = input("Ingrese sus apellidos: ")
    tipo_documento = input("Ingrese el tipo de documento, por ejemplo CC: ")
    numero_documento = input("Ingrese el número de documento: ")

    print()
    print("Candidatos disponibles:")

    for candidato in votos:
        print(f"- {candidato}")

    candidato = input("Ingrese el candidato por el que desea votar: ")

    resultado = registrar_voto(
        nombre,
        apellidos,
        tipo_documento,
        numero_documento,
        candidato
    )

    print()
    print(resultado)


if __name__ == "__main__":
    iniciar_votacion()
