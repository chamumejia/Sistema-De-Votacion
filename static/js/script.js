function confirmarReinicio() {
    return window.confirm(
        "¿Seguro que deseas reiniciar la votación? " +
        "El resultado actual se guardará en el historial."
    );
}

document.addEventListener("DOMContentLoaded", function () {
    const alertas = document.querySelectorAll(".alerta");

    alertas.forEach(function (alerta) {
        setTimeout(function () {
            alerta.style.opacity = "0";
            alerta.style.transition = "opacity .4s ease";

            setTimeout(function () {
                alerta.remove();
            }, 500);
        }, 5000);
    });
});
