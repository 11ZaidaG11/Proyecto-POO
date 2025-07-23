import flet as ft
import io
import base64
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg

from backend.modulo1 import NaturalFile, Translator, Grapher, GCodeFile, tool

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


def graficar(e, image_control: ft.Image):
    tool.current_X = 0
    tool.current_y = 0

    grapher = Grapher(GCodeFile())

    # Crear figura de matplotlib
    fig, ax = plt.subplots(figsize=(10, 8), dpi=100)
    grapher.graph(ax=ax)
    ax.axis('equal')           
    ax.grid(True)
    ax.set_title("Simulación CNC")

    # Renderizar figura en memoria
    buf = io.BytesIO()
    canvas = FigureCanvasAgg(fig)
    canvas.draw()
    canvas.print_png(buf)
    buf.seek(0)

    # Codificar en base64 para Flet
    img_base64 = base64.b64encode(buf.read()).decode("utf-8")
    image_control.src_base64 = img_base64
    image_control.update()
