import re
import matplotlib.pyplot as plt
import numpy as np
import math
import flet as ft
import asyncio

# Area de trabajo de la máquina CNC
class WorkArea:
    max_width = 300
    max_height = 200

# Lámina para cortar
class Sheet:
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    # Verifica si la lámina cabe en work area
    def is_in_bounds(self, sheet: "Sheet", work_area: WorkArea) -> bool:
        return sheet.width <= work_area.max_width and sheet.height <= work_area.max_height  

# Herramienta de corte
class CutterTool:
    def __init__(self, x: float, y: float): # Hay que conocer su posición en todo momento
        self.current_X = x
        self.current_Y = y

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

# Traductor de lenguaje natural a GCode
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

    def __init__(self, n_file: NaturalFile, tool: CutterTool, g_file: GCodeFile):
        # Busca en natural_file las expresiones regulares
        self.content = n_file.read_file()
<<<<<<< HEAD
        self.current_X = 0.0 
        self.current_Y = 0.0

    def translate(self) -> GCodeFile:
        lines: list = []
        for line in self.content.strip().splitlines():
            line = line.strip()
            m1 = re.match(self.patt1, line)
            if m1:
                G = self.dictionary[m1.group(1)]
                X = m1.group(2)
                Y = m1.group(3)
                lines.append(f"{G} X{X} Y{Y}\n")
                self.current_X, self.current_Y = float(X), float(Y)
                continue

            m2 = re.match(self.patt2, line)
            if m2:
                G = self.dictionary[m2.group(1)]
                X = m2.group(2)
                Y = m2.group(3)
                preI = float(m2.group(4))
                preJ = float(m2.group(5))
                I = preI - self.current_X
                J = preJ - self.current_Y
                lines.append(f"{G} X{X} Y{Y} I{I} J{J}\n")
                self.current_X, self.current_Y = float(X), float(Y)
                continue
            
        nat_to_gc = "".join(lines)
        g_file.write_file(nat_to_gc)
        return g_file

g_file = GCodeFile()
tool = CutterTool(0,0)
=======
        self.match1 = re.finditer(self.patt1, self.content, re.MULTILINE)
        self.match2 = re.finditer(self.patt2, self.content, re.MULTILINE)

        self.tool = tool
        self.g_file = g_file

    def translate(self) -> GCodeFile:
        lines: list = [] # Guarda las líneas de GCode
        if self.match1:
            for m in self.match1:
                G = self.dictionary[m.group(1)]
                X = m.group(2)
                Y = m.group(3)

                # Escribe la línea Gcode
                line = f"{G} X{X} Y{Y}\n"
                lines.append(line)

                # Actualiza la posición actual
                self.tool.current_X = X
                self.tool.current_Y = Y 

        if self.match2:
            for m in self.match2:
                G = self.dictionary[m.group(1)]
                X = m.group(2)
                Y = m.group(3)
                preI = m.group(4)
                preJ = m.group(5)
                
                # Calcula el centro relativo a la posición de la herramienta
                I = float(preI) - float(self.tool.current_X)
                J = float(preJ) - float(self.tool.current_Y)
                line = f"{G} X{X} Y{Y} I{I} J{J}\n"
                lines.append(line)
                self.tool.current_X = X
                self.tool.current_Y = Y
        
        nat_to_gc = "".join(lines) # Une las líneas en un string
        self.g_file.write_file(nat_to_gc)
        return self.g_file # Devuelve el archivo GCode
>>>>>>> 43c7fc2f9a9aeb882995d75329377dbebe45ca18

class Grapher:
    # Expresiones regulares para instrucciones GCode
    mov_rapido = r"(G00) X(-?\d+(?:\.\d+)?) Y(-?\d+(?:\.\d+)?)"
    mov_lineal = r"(G01) X(-?\d+(?:\.\d+)?) Y(-?\d+(?:\.\d+)?)"
    mov_circ_h = r"(G02) X(-?\d+(?:\.\d+)?) Y(-?\d+(?:\.\d+)?) I(-?\d+(?:\.\d+)?) J(-?\d+(?:\.\d+)?)"
    mov_circ_antih = r"(G03) X(-?\d+(?:\.\d+)?) Y(-?\d+(?:\.\d+)?) I(-?\d+(?:\.\d+)?) J(-?\d+(?:\.\d+)?)"

    def __init__(self, g_file: GCodeFile, tool: CutterTool):
        self.content = g_file.read_file()
        self.tool = tool

    def graph(self, ax=None):
        if ax is None:
            ax = plt.gca()

        puntos = [(self.tool.current_X, self.tool.current_Y)]

        # Buscar todas las instrucciones en orden
        patron = f"{self.mov_rapido}|{self.mov_lineal}|{self.mov_circ_h}|{self.mov_circ_antih}"
        matches = list(re.finditer(patron, self.content, re.MULTILINE))

        for m in matches:
            if m.group(1) == "G00":
                x = float(m.group(2))
                y = float(m.group(3))
                ax.plot([self.tool.current_X, x], [self.tool.current_Y, y], 'k--')
                self.tool.current_X, self.tool.current_Y = x, y
                puntos.append((x, y))

            elif m.group(4) == "G01":
                x = float(m.group(5))
                y = float(m.group(6))
                ax.plot([self.tool.current_X, x], [self.tool.current_Y, y], 'b-')
                self.tool.current_X, self.tool.current_Y = x, y
                puntos.append((x, y))

            elif m.group(7) == "G02":
                x = float(m.group(8))
                y = float(m.group(9))
                I = float(m.group(10))
                J = float(m.group(11))
                self.dibujar_arco(ax, x, y, I, J, sentido="horario", puntos=puntos)

            elif m.group(12) == "G03":
                x = float(m.group(13))
                y = float(m.group(14))
                I = float(m.group(15))
                J = float(m.group(16))
                self.dibujar_arco(ax, x, y, I, J, sentido="antihorario", puntos=puntos)

        xs, ys = zip(*puntos)
        margin = 10
        ax.set_xlim(min(xs) - margin, max(xs) + margin)
        ax.set_ylim(min(ys) - margin, max(ys) + margin)
        ax.set_aspect('equal')

<<<<<<< HEAD
    def dibujar_arco(self, ax, x, y, I, J, sentido, puntos):
        cx = tool.current_X + I
        cy = tool.current_y + J
=======
    def _dibujar_arco(self, ax, x, y, I, J, sentido, puntos):
        cx = self.tool.current_X + I
        cy = self.tool.current_Y + J
>>>>>>> 43c7fc2f9a9aeb882995d75329377dbebe45ca18
        r = np.sqrt(I**2 + J**2)

        start_ang = np.arctan2(self.tool.current_Y - cy, self.tool.current_X - cx)
        end_ang = np.arctan2(y - cy, x - cx)

        if sentido == "horario":
            if end_ang > start_ang:
                end_ang -= 2 * np.pi
        else: # antihorario
            if end_ang < start_ang:
                end_ang += 2 * np.pi

        theta = np.linspace(start_ang, end_ang, 100)
        x_arc = cx + r * np.cos(theta)
        y_arc = cy + r * np.sin(theta)

        ax.plot(x_arc, y_arc, 'r-')
        self.tool.current_X, self.tool.current_Y = x, y
        puntos.append((x, y))

<<<<<<< HEAD
class WorkArea:
    def __init__(self, max_width: float, max_height: float):
        self.max_width = max_width
        self.max_height = max_height

    def is_in_bounds(self, sheet_width: float, sheet_height: float) -> bool:
        return sheet_width <= self.max_width and sheet_height <= self.max_height

class ManualUsuario:
    def __init__(self, page: ft.Page):
        self.page = page
        self.dialog = ft.AlertDialog(
            modal=True,
            shape=ft.RoundedRectangleBorder(radius=20),
            bgcolor="#e2d6ff",
            title=ft.Text(
                "Manual de usuario",
                font_family="Press Start 2P",
                size=20,
                weight=ft.FontWeight.BOLD,
                color="#5f00ad",
                text_align=ft.TextAlign.CENTER
            ),
            title_padding=ft.padding.only(20, 20, 20, 0),
            content=ft.Container(
                width=600,
                height=400,
                padding=ft.padding.all(20),
                content=ft.Column(
                    scroll=ft.ScrollMode.AUTO,
                    controls=[
                        ft.Text(
                            self.texto_manual(),
                            font_family="Space Mono",
                            size=16,
                            color="black",
                            text_align=ft.TextAlign.JUSTIFY
                        )
                    ]
                )
            ),
            actions=[
                ft.TextButton(
                    "Cerrar",
                    on_click=self.close,
                    style=ft.ButtonStyle(
                        color={"": "#b484db"},
                        padding=ft.padding.symmetric(horizontal=20, vertical=10),
                        text_style=ft.TextStyle(font_family="Space Mono", size=14)
                    )
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        self.page.overlay.append(self.dialog)

    def texto_manual(self):
        return (
            "Este software permite controlar un sistema CNC de forma remota. "
            "En el menú lateral puedes describir, visualizar su ruta de ejecución "
            "y controlar parámetros de velocidad y posición. "
            "\n\nPasos sugeridos:\n"
            "1. Carga tu archivo desde el botón 'Cargar G-code'.\n"
            "2. Verifica la vista previa de trayectorias.\n"
            "3. Usa los controles de simulación o ejecución real para iniciar el proceso.\n"
            "4. Consulta los reportes de ejecución desde la pestaña correspondiente.\n"
            "\nEste manual se irá actualizando con nuevas versiones."
        )

    def open_manual(self, e):
        print("Abriendo manual de usuario.")
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.update()

    def close(self, e):
        self.dialog.open = False
        self.page.update()


class ErrorTamano:
    def __init__(self, page: ft.Page, mensaje_error: str, duracion=3):
        self.page = page
        self.mensaje_error = mensaje_error
        self.duracion = duracion

        self.dialog = ft.AlertDialog(
            modal=True,
            shape=ft.ContinuousRectangleBorder(radius=20),
            bgcolor="#ffd6de",
            title=ft.Text(
                "Error",
                font_family="Press Start 2P",
                size=15,
                weight=ft.FontWeight.BOLD,
                color="#ad0056",
                text_align=ft.TextAlign.CENTER
            ),
            title_padding=ft.padding.only(20, 20, 20, 0),
            content=None
        )

        self.page.overlay.append(self.dialog)

    async def mostrar(self):
        self.dialog.content = ft.Container(
            width=220,
            height=140,
            padding=ft.padding.all(20),
            content=ft.Column(
                scroll=ft.ScrollMode.AUTO,
                controls=[
                    ft.Text(
                        self.mensaje_error,
                        font_family="Space Mono",
                        size=16,
                        color="black",
                        text_align=ft.TextAlign.JUSTIFY
                    )
                ]
            )
        )

        self.dialog.open = True
        self.page.update()
        await asyncio.sleep(self.duracion)
        self.dialog.open = False
        self.page.update()
=======
work_area = WorkArea()
tool = CutterTool(0, 0)
>>>>>>> 43c7fc2f9a9aeb882995d75329377dbebe45ca18
