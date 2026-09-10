candidatos = {
    "Ana": 0,
    "Carlos": 0,
    "Luisa": 0
}

registro_votos = {}

HISTORIAL = "historial_votacion.txt"


def registrar_voto(persona, candidato):
    pass


def ver_resultados():
    pass


def reiniciar_votacion():
    pass


def mostrar_menu():
    while True:
        print("\n--- SISTEMA DE VOTACIÓN ---")
        print("1. Registrar voto")
        print("2. Ver resultados")
        print("3. Reiniciar votación")
        print("4. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            persona = input("Nombre de la persona: ")
            candidato = input("Candidato: ")
            registrar_voto(persona, candidato)

        elif opcion == "2":
            ver_resultados()

        elif opcion == "3":
            reiniciar_votacion()

        elif opcion == "4":
            print("Programa finalizado.")
            break

        else:
            print("Opción inválida.")


if __name__ == "__main__":
    mostrar_menu()
