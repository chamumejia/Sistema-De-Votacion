import json
from pathlib import Path

from werkzeug.security import generate_password_hash, check_password_hash
from actividad import registrar_actividad


ARCHIVO_USUARIOS = Path("usuarios.txt")


def cargar_usuarios():
    if not ARCHIVO_USUARIOS.exists():
        return {}

    try:
        with ARCHIVO_USUARIOS.open("r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except (json.JSONDecodeError, OSError):
        return {}


def guardar_usuarios(usuarios):
    with ARCHIVO_USUARIOS.open("w", encoding="utf-8") as archivo:
        json.dump(usuarios, archivo, indent=4, ensure_ascii=False)


def registrar_usuario(
    nombre,
    apellidos,
    tipo_documento,
    numero_documento,
    usuario,
    password
):
    nombre = nombre.strip()
    apellidos = apellidos.strip()
    tipo_documento = tipo_documento.strip().upper()
    numero_documento = numero_documento.strip()
    usuario = usuario.strip().lower()

    if not all([
        nombre,
        apellidos,
        tipo_documento,
        numero_documento,
        usuario,
        password
    ]):
        registrar_actividad("Registro rechazado: faltan datos")
        return False, "Todos los campos son obligatorios."

    usuarios = cargar_usuarios()
    documento = f"{tipo_documento}:{numero_documento}"

    if documento in usuarios:
        registrar_actividad(
            f"Registro rechazado: documento {documento} ya existe"
        )
        return False, "Ya existe una cuenta con ese documento."

    for datos in usuarios.values():
        if datos["usuario"] == usuario:
            registrar_actividad(
                f"Registro rechazado: usuario {usuario} ya existe"
            )
            return False, "Ese nombre de usuario ya está registrado."

    usuarios[documento] = {
        "nombre": nombre,
        "apellidos": apellidos,
        "tipo_documento": tipo_documento,
        "numero_documento": numero_documento,
        "usuario": usuario,
        "password": generate_password_hash(password)
    }

    guardar_usuarios(usuarios)
    registrar_actividad(f"Usuario registrado: {usuario}")

    return True, "Cuenta creada correctamente."


def autenticar_usuario(usuario, password):
    usuario = usuario.strip().lower()
    usuarios = cargar_usuarios()

    for datos in usuarios.values():
        if (
            datos["usuario"] == usuario
            and check_password_hash(datos["password"], password)
        ):
            registrar_actividad(f"Inicio de sesión correcto: {usuario}")
            return datos

    registrar_actividad(f"Inicio de sesión fallido: {usuario}")
    return None
