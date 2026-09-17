from functools import wraps

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for
)

from actividad import registrar_actividad
from registro_votos import (
    registrar_voto,
    reiniciar_votacion,
    ver_resultados
)
from usuarios import autenticar_usuario, registrar_usuario


app = Flask(__name__)
app.config["SECRET_KEY"] = "clave-secreta-votacion"


def usuario_requerido(funcion):
    @wraps(funcion)
    def revisar_sesion(*args, **kwargs):
        if "usuario" not in session:
            flash(
                "Debes iniciar sesión para continuar.",
                "warning"
            )
            return redirect(url_for("login"))

        return funcion(*args, **kwargs)

    return revisar_sesion


@app.route("/")
def inicio():
    return render_template("inicio.html")


@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        correcto, mensaje = registrar_usuario(
            request.form.get("nombre", ""),
            request.form.get("apellidos", ""),
            request.form.get("tipo_documento", ""),
            request.form.get("numero_documento", ""),
            request.form.get("usuario", ""),
            request.form.get("password", "")
        )

        if correcto:
            flash(mensaje, "success")
            return redirect(url_for("login"))

        flash(mensaje, "danger")

    return render_template("registro.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        datos = autenticar_usuario(
            request.form.get("usuario", ""),
            request.form.get("password", "")
        )

        if datos:
            session["usuario"] = datos["usuario"]
            session["datos_usuario"] = datos

            flash(
                f"Bienvenido, {datos['nombre']}.",
                "success"
            )

            return redirect(url_for("votar"))

        flash("Usuario o contraseña incorrectos.", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    usuario = session.get("usuario", "desconocido")
    registrar_actividad(f"Sesión cerrada: {usuario}")

    session.clear()
    flash("Sesión cerrada correctamente.", "success")

    return redirect(url_for("inicio"))


@app.route("/votar", methods=["GET", "POST"])
@usuario_requerido
def votar():
    datos_usuario = session["datos_usuario"]

    if request.method == "POST":
        correcto, mensaje = registrar_voto(
            datos_usuario["nombre"],
            datos_usuario["apellidos"],
            datos_usuario["tipo_documento"],
            datos_usuario["numero_documento"],
            request.form.get("candidato", "")
        )

        if correcto:
            flash(mensaje, "success")
            return redirect(url_for("resultados"))

        flash(mensaje, "danger")

    return render_template(
        "votar.html",
        datos_usuario=datos_usuario
    )


@app.route("/resultados")
@usuario_requerido
def resultados():
    datos, total = ver_resultados()

    return render_template(
        "resultados.html",
        resultados=datos,
        total=total
    )


@app.route("/reiniciar", methods=["POST"])
@usuario_requerido
def reiniciar():
    reiniciar_votacion()

    flash(
        "La votación fue reiniciada y el resultado anterior "
        "se guardó en el historial.",
        "success"
    )

    return redirect(url_for("resultados"))


if __name__ == "__main__":
    app.run(debug=True)
