import tkinter as tk
import math
import re

# Clase que representa la lámina: 
class Sheet:
    def __init__(self, material: str, size: list[float]):
        self.material = material
        self.size = size

# El archivo con instrucciones en lenguaje natural
class NaturalFile:
    name: str = "natural_file.txt"

    def __init__(self):
        self.nf_content = self.read_file()
    
    def write_file(self): #! natural_tf.value: str
        with open(self.name, "w", encoding="utf-8") as nf:
            nf.write() #! natural_tf.value
    
    def read_file(self):
        with open(self.name, "r", encoding="utf-8") as nf:
            return nf.read()
        
# El archivo con las instrucciones G-Code
class GCodeFile:
    name: str = "gcode_file.txt"

    def __init__(self):
        self.gf_content = self.read_file()
    
    def write_file(self, text: str):
        with open(self.name, "w", encoding="utf-8") as gf:
            gf.write(text)

    def read_file(self):
        with open(self.name, "r", encoding="utf-8") as gf:
            return gf.read()
    
# El resultado final luego de hacer el corte a la Sheet
class ModifiedSheet(Sheet):
    def __init__(self, material, size):
        super().__init__(material, size)

# EL área de trabajo de la máquina de CNC
class WorkArea:
    def __init__(self, size: tuple[float, float, float]):
        self.size = size

# Herramienta de corte 
class CutterTool:
    def __init__(self, x:float, y:float):
        self.current_X = x
        self.current_y = y
        self.active = False
    
    def apply(self, sheet: Sheet, gcode: GCodeFile): # -> Modified Sheet
        # incluir aquí la lógica para aplicar el G-Code al Sheet
        print(f"Aplicando {gcode.name} sobre la lámina de {sheet.material}")
        return ModifiedSheet(sheet.material, sheet.size)

    def activate_tool(self):
        self.active = True
        print("La herramienta ha sido activada.")

    def deactivate_tool(self):
        self.active = False
        print("Herramienta desactivada.")

# Traductor entre el lenguaje natural y el G-Code
class Translator:
    dictionary = {
        "Ubicar": "G00",
        "Recta": "G01",
        "horario": "G02",
        "antihorario": "G03"
    }

    # Expresiones regulares
    patt1 = r"(Ubicar|Recta): (-?\d+(?:\.\d+)?), (-?\d+(?:\.\d+)?)"
    patt2 = r"Arco (horario|antihorario): (-?\d+(?:\.\d+)?), (-?\d+(?:\.\d+)?); Centro: (-?\d+(?:\.\d+)?), (-?\d+(?:\.\d+)?)"

    def __init__(self, n_file: NaturalFile):
        self.content = n_file.nf_content
        self.match1 = re.finditer(self.patt1, self.content, re.MULTILINE)
        self.match2 = re.finditer(self.patt2, self.content, re.MULTILINE)

    def translate(self, tool: CutterTool, g_file: GCodeFile) -> GCodeFile:
        lines: list = []
        if self.match1:
            for m in self.match1:
                G = self.dictionary[m.group(1)]
                X = m.group(2)
                Y = m.group(3)
                line = f"{G} X{X} Y{Y}\n"
                lines.append(line)

        if self.match2:
            for m in self.match2:
                G = self.dictionary[m.group(1)]
                X = m.group(2)
                Y = m.group(3)
                preI = m.group(4)
                preJ = m.group(5)
                I = tool.current_X - float(preI)
                J = tool.current_y - float(preJ)
                line = f"{G} X{X} Y{Y} I{I} J{J}\n"
                lines.append(line)
        
        nat_to_gc = "".join(lines)
        g_file.write_file(nat_to_gc)
        return g_file
    
# Máquina de CNC que maneja TODO
class CNCMachine:
    def __init__(self, name: str, work_area: WorkArea, tool: CutterTool, \
                 translator: Translator):
        self.name = name
        self.work_area = work_area
        self.tool = tool
        self.translator = translator

    def start(self):
        print(f"{self.name} inciando")
        

    def stop(self):
        print(f"{self.name} deteniéndose")


#-----------------------------------------------------------------------
# Función para convertir parámetros G-Code en valores para tkinter


def gcode_a_createarc(x_inicial, y_inicial, x_final, y_final, i, j,\
                       sentido_horario=True):
    # calcular el centro del circulo o elipse
    cx = x_inicial + i
    cy = y_inicial + j
    radio = math.hypot(i, j)

    # se calculan los vertices del rectangulo delimitador
    x0 = cx - radio
    y0 = cy - radio
    x1 = cx + radio
    y1 = cy + radio

    # se calcula el angulo que hay entre el eje x y el vector que va del 
    # centro al inicio del arco, respecto al eje x
    angulo_inicial = math.degrees(math.atan2(y_inicial - cy, x_inicial - cx)) % 360
    #se calcula el angulo que hay entre el eje x y el vector que va del centro al final del arco
    angulo_final = math.degrees(math.atan2(y_final - cy, x_final - cx)) % 360
    
    if sentido_horario:
        extent = (angulo_inicial - angulo_final) % 360
        extent = -extent  # sentido horario
    else:
        extent = (angulo_final - angulo_inicial) % 360
    return {
        "x0": x0,
        "y0": y0,
        "x1": x1,
        "y1": y1,
        "start": angulo_inicial,
        "extent": extent
    }

#-----------------------------------------------------------------------
# DEMO: Dibujar arco G-Code en canvas
#-----------------------------------------------------------------------

# Datos de prueba: simulación de G-code
gcode = [
    "G0 X50 Y50",   # Ir al punto inicial (sin dibujar)
    "G1 X200 Y50",  # Línea horizontal
    "G1 X200 Y200", # Línea vertical
    "G1 X50 Y200",  # Línea horizontal inversa
    "G1 X50 Y50"    # Cierre del cuadrado
]

# Crear ventana de tkinter
root = tk.Tk()
root.title("Visualización de Arco G-code")

canvas = tk.Canvas(root, width=300, height=300, bg="white")
canvas.pack()

# Datos de ejemplo (G2: arco horario)
x_start, y_start = 100, 100
x_end, y_end = 150, 100
i, j = 25, 0  # centro a 25 px a la derecha (125, 100)

# Obtener parámetros del arco
params = gcode_a_createarc(x_start, y_start, x_end, y_end, i, j, sentido_horario=True)

canvas.create_arc(
    params["x0"], params["y0"], params["x1"], params["y1"],
    start=params["start"],
    extent=params["extent"],
    style="arc",
    outline="red"
)

root.mainloop()
