import flet as ft
from backend.modulo1 import NaturalFile, Translator


def mai(page: ft.Page):
    page.title = "Simulador CNC"

    natural_tf = ft.TextField(
        label="Lenguaje natural",
        multiline=True,
        min_lines=1,
        max_lines=11,
    )


    def natural_file(e):
        cont = natural_tf.value                      # ✅ Captura el texto primero

        naturalf = NaturalFile()                     # ✅ Instancia el archivo
        naturalf.write_file(cont)                    # ✅ Escribe antes que nada
        print("natural file saved")

        traductor = Translator(naturalf)             # ✅ Instancia el traductor después de escribir
        gcode = traductor.translate()                # ✅ Ahora sí traduce con el archivo nuevo

        gcode_tf.value = gcode.__str__()
        print("Translated")
        print(gcode_tf.value)
        page.update()


    traductor_but = ft.ElevatedButton(on_click=natural_file, text="Traducir")

    # Mostrar el G-Code generado (cuando se genere automáticamente)
    gcode_tf = ft.TextField(
        label="Código G",
        multiline=True,
        min_lines=1,
        max_lines=11,
        read_only=True
    )

    # El botón copiar copia el G-Code al portapapeles
    def copy_gcode(e):
        page.set_clipboard(gcode_tf.value)

    copy_but = ft.ElevatedButton(on_click=copy_gcode, text="Copiar")

    page.add(natural_tf, traductor_but, gcode_tf, copy_but)