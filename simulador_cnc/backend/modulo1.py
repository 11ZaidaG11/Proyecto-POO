import re
import matplotlib.pyplot as plt
import numpy as np


# El archivo con instrucciones en lenguaje natural
class NaturalFile:
    name: str = "natural_file.txt"

    def write_file(self, text): 
        with open(self.name, "w", encoding="utf-8") as nf:
            nf.write(text)

    def read_file(self):
        with open(self.name, "r", encoding="utf-8") as nf:
            return nf.read()

    def clean_file(self):
        with open(self.name, "w", encoding="utf-8") as nf:
            nf.write("")

# El archivo con las instrucciones G-Code
class GCodeFile:
    name: str = "gcode_file.txt"
    
    def write_file(self, text: str):
        with open(self.name, "w", encoding="utf-8") as gf:
            gf.write(text)
            
    def read_file(self):
        with open(self.name, "r", encoding="utf-8") as gf:
            return gf.read()

    def clean_file(self):
        with open(self.name, "w", encoding="utf-8") as gf:
            gf.write("")
        
    def __str__(self):
        return self.read_file()
    
# Herramienta de corte 
class CutterTool:
    def __init__(self, x:float, y:float):
        self.current_X = x
        self.current_y = y

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
        self.content = n_file.read_file()
        self.match1 = re.finditer(self.patt1, self.content, re.MULTILINE)
        self.match2 = re.finditer(self.patt2, self.content, re.MULTILINE)

    def translate(self) -> GCodeFile:
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

g_file = GCodeFile()
tool = CutterTool(0,0)

class Grapher:
    # Posibles salidas del traductor de lenguaje natural a gcode
    mov_rapido = r"(G00) X(-?\d+(?:\.\d+)?) Y(-?\d+(?:\.\d+)?)"
    mov_lineal = r"(G01) X(-?\d+(?:\.\d+)?) Y(-?\d+(?:\.\d+)?)"
    mov_circ_h = r"(G02) X(-?\d+(?:\.\d+)?) Y(-?\d+(?:\.\d+)?) I(-?\d+(?:\.\d+)?) J(-?\d+(?:\.\d+)?)"
    mov_circi_antih = r"(G03) X(-?\d+(?:\.\d+)?) Y(-?\d+(?:\.\d+)?) I(-?\d+(?:\.\d+)?) J(-?\d+(?:\.\d+)?)"

    def __init__(self, g_file: GCodeFile):
        self.content = g_file.read_file()
        self.match0 = re.finditer(self.mov_rapido, self.content, re.MULTILINE)
        self.match1 = re.finditer(self.mov_lineal, self.content, re.MULTILINE)
        self.match2 = re.finditer(self.mov_circ_h, self.content, re.MULTILINE)
        self.match3 = re.finditer(self.mov_circi_antih, self.content, re.MULTILINE)

    def graph(self,ax=None):
        if ax is None:
            ax=plt.gca()

        puntos = [(tool.current_X, tool.current_y)]

        for m in self.match0:
            x = float(m.group(2))
            y = float(m.group(3))
            ax.plot([tool.current_X,x],[tool.current_y,y], 'k--')
            tool.current_X, tool.current_y = x, y
            puntos.append((x, y))

        for m in self.match1:
            x = float(m.group(2))
            y = float(m.group(3))
            ax.plot([tool.current_X,x],[tool.current_y,y], 'b-')
            tool.current_X, tool.current_y = x, y
            puntos.append((x, y))

        for m in self.match2:
            #punto final del arco
            x = float(m.group(2))
            y = float(m.group(3))
            #centro relativo del arco
            I = float(m.group(4))
            J = float(m.group(5))

            #centro absoluto (se suman las coordenadas de la maquina a las del centro relativo ya que la maquina no siempre estara ubicada en 0)
            centro_x = tool.current_X + I
            centro_y = tool.current_y + J

            #radio del arco
            r = np.sqrt(I**2 + J**2)

            #anulo inicial y final (angulo de la maquina al punto inicial del arco y de la maquina al punto final respectivamente)
            angle_start = np.arctan2(tool.current_y - centro_y, tool.current_X - centro_x)
            angle_end = np.arctan2(y - centro_y, x - centro_x)

            if angle_end > angle_start:
                angle_end -= 2 * np.pi

            #se generan 100 valores angulares entre el angulo inicial y final
            theta = np.linspace(angle_start, angle_end, 100)

            #puntos del arco (se usa la ecuacion parametrica de un circulo)
            x_arc = centro_x + r * np.cos(theta)
            y_arc = centro_y + r * np.sin(theta)

            ax.plot(x_arc, y_arc, 'r-')
            tool.current_X, tool.current_y = x, y
            puntos.append((x, y))

        for m in self.match3:
            #punto final del arco
            x = float(m.group(2))
            y = float(m.group(3))
            #centro relativo del arco
            I = float(m.group(4))
            J = float(m.group(5))

            #centro absoluto (se suman las coordenadas de la maquina a las del centro relativo ya que la maquina no siempre estara ubicada en 0)
            centro_x = tool.current_X + I
            centro_y = tool.current_y + J

            #radio del arco
            r = np.sqrt(I**2 + J**2)

            #anulo inicial y final (angulo de la maquina al punto inicial del arco y de la maquina al punto final respectivamente)
            angle_start = np.arctan2(tool.current_y - centro_y, tool.current_X - centro_x)
            angle_end = np.arctan2(y - centro_y, x - centro_x)

            if angle_end < angle_start:
                angle_end += 2 * np.pi

                
            #se generan 100 valores angulares entre el angulo inicial y final
            theta = np.linspace(angle_start, angle_end, 100)

            #puntos del arco (se usa la ecuacion parametrica de un circulo)
            x_arc = centro_x + r * np.cos(theta)
            y_arc = centro_y + r * np.sin(theta)

            ax.plot(x_arc, y_arc, 'r-')
            tool.current_X, tool.current_y = x, y
            puntos.append((x, y))

        # Extrae coordenadas X e Y
        xs, ys = zip(*puntos)
        margin = 10
        y_center = (min(ys) + max(ys)) / 2
        y_range = (max(ys) - min(ys)) / 2 + 10
        ax.set_xlim(min(xs) - margin, max(xs) + margin)
        ax.set_ylim(min(ys) - margin, max(ys) + margin)