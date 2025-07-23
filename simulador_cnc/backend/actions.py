from backend.modulo1 import NaturalFile, Translator, Grapher, GCodeFile, tool
from backend.modulo1 import WorkArea, ErrorTamano
import flet as ft
import matplotlib.pyplot as plt
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg
import base64
import asyncio


class CNCMachine:
    def __init__(self, max_width=300, max_height=200):
        self.natural_file = NaturalFile()
        self.gcode_file = GCodeFile()
        self.translator = None
        self.grapher = None
        self.tool = tool
        self.work_area = WorkArea(max_width, max_height)

    def load_natural_instructions(self, text: str):
        self.natural_file.write_file(text)
        self.translator = Translator(self.natural_file)

    def translate_to_gcode(self):
        if not self.translator:
            raise Exception("No se ha cargado ningún archivo de instrucciones.")
        self.gcode_file = self.translator.translate()
        return str(self.gcode_file)

    def generate_grapher(self):
        self.grapher = Grapher(self.gcode_file)
        return self.grapher

    def validate_sheet(self, width: float, height: float) -> bool:
        return self.work_area.is_in_bounds(width, height)


cnc=CNCMachine()
# Crea un archivo de texto con el input de natural_tf
def natural_file(e, gcode_tf, natural_tf, pag, sheet_tf):
    cont = natural_tf.value

    # Verifica que la lámina tenga el formato correcto ("ancho x alto")
    async def validar_datos():
        lamina_ingresada = sheet_tf.value.strip()
        if "x" not in lamina_ingresada:
            error_dialog = ErrorTamano(pag, "Usa el formato: ancho x alto, por ejemplo: 300x200")
            await error_dialog.mostrar()
            return False


        try:
            ancho_txt, alto_txt = lamina_ingresada.split("x")
            sheet_width = float(ancho_txt)
            sheet_height = float(alto_txt)
        except ValueError:
            error_dialog = ErrorTamano(pag, "Los valores deben ser números válidos.")
            await error_dialog.mostrar()
            return False

        if not cnc.validate_sheet(sheet_width, sheet_height):
            error_dialog = ErrorTamano(pag, "La lámina excede el tamaño permitido (300x200 mm).")
            await error_dialog.mostrar()
            return False
        return True


    # Ejecutar validación
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            validacion = asyncio.ensure_future(validar_datos())
            return  # no continuar aún, se ejecutará aparte
        else:
            validacion = asyncio.run(validar_datos())
    except RuntimeError:
        validacion = asyncio.run(validar_datos())

    if not validacion:
        return

    # Si todo está bien, continúa con la traducción
    cnc.load_natural_instructions(cont)
    gcode_tf.value = cnc.translate_to_gcode()

    print("natural file saved")
    print("Translated")
    print(gcode_tf.value)
    pag.update()



def copy_gcode(e, gcode_tf, pag):
    pag.set_clipboard(gcode_tf.value)


def graficar(e, image_control: ft.Image):
    tool.current_X = 0
    tool.current_y = 0

    grapher = cnc.generate_grapher()

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