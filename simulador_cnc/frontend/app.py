# Se importa Flet para la interfaz gráfica
import flet as ft
from simulador_cnc.backend.modulo1 import NaturalFile

# función para recibir la "página" (interfaz principal)
def main(pag: ft.Page):
    pag.title = "Simulador CNC"    

# Campo para escribir en lenguaje natural
    natural_tf = ft.TextField(
        label="Lenguaje natural",
        multiline=True,
        min_lines=1,
        max_lines=11,
    )

    # Crea un archivo de texto con el input de natural_tf
    naturalf = NaturalFile()

    traductor_but = ft.ElevatedButton(
        on_click=naturalf.write_file(natural_tf.value),
        text="Traducir",
    )

    pag.add(
        natural_tf, traductor_but
    )

# Ejecutar la app
ft.app(main, assets_dir="assets")