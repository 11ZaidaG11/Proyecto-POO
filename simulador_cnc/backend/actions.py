from backend.modulo1 import NaturalFile, Translator, Grapher, GCodeFile, tool
from backend.modulo1 import WorkArea, work_area
import flet as ft
import matplotlib.pyplot as plt
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg
import base64

# Crea un archivo de texto con el input de natural_tf
def natural_file(e, gcode_tf, natural_tf, pag, sheet_tf):
    cont = natural_tf.value

    # Verifica que la lámina tenga el formato correcto ("ancho x alto")
    lamina_ingresada = sheet_tf.value.strip()
    if "x" not in lamina_ingresada:
        pag.snack_bar.content = ft.Text("⚠️ Usa el formato: ancho x alto, por ejemplo: 300x200")
        pag.snack_bar.bgcolor = "#FFF59D"
        pag.snack_bar.open = True
        pag.update()
        return

    ancho_txt, alto_txt = lamina_ingresada.split("x")

    try:
        sheet_width = float(ancho_txt)
        sheet_height = float(alto_txt)
    except ValueError:
        pag.snack_bar.content = ft.Text("⚠️ Los valores deben ser números válidos.")
        pag.snack_bar.bgcolor = "#EF9A9A"
        pag.snack_bar.open = True
        pag.update()
        return

    if not work_area.is_in_bounds(sheet_width, sheet_height):
        pag.snack_bar.content = ft.Text("❌ La lámina excede el tamaño permitido (300x200 mm)")
        pag.snack_bar.bgcolor = "#EF9A9A"
        pag.snack_bar.open = True
        pag.update()
        return

    # Si todo está bien, continúa con la traducción
    naturalf = NaturalFile()
    naturalf.write_file(cont)
    print("natural file saved")

    traductor = Translator(naturalf)
    gcode = traductor.translate()

    gcode_tf.value = str(gcode)
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

def vaciar(e, natural_tf, gcode_tf, sheet_tf, pag):
    natural_tf.value = ""
    gcode_tf.value = ""
    sheet_tf.value = ""
    pag.snack_bar = ft.SnackBar(ft.Text("Campos vaciados correctamente"))
    pag.snack_bar.open = True
    pag.update()