from backend.modulo1 import NaturalFile, Translator
import flet as ft

# Crea un archivo de texto con el input de natural_tf
def natural_file(e, gcode_tf, natural_tf, pag):
    cont = natural_tf.value

    naturalf = NaturalFile()
    naturalf.write_file(cont)
    print("natural file saved")

    traductor = Translator(naturalf)
    gcode = traductor.translate()

    gcode_tf.value = gcode.__str__()
    print("Translated")
    print(gcode_tf.value)
    pag.update()

def copy_gcode(e, gcode_tf, pag):
    pag.set_clipboard(gcode_tf.value)
