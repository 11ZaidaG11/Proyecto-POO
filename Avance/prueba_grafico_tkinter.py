import math
import tkinter as tk

def gcode_a_createarc(x_inicial, y_inicial, x_final, y_final, i, j, sentido_horario=True):
    #calcular el centro del circulo o elipse
    cx=x_inicial+i
    cy=y_inicial+j
    radio=math.hypot(i,j)

    #se calculan los vertices del rectangulo
    x0 = cx - radio
    y0 = cy - radio
    x1 = cx + radio
    y1 = cy + radio
    #se calcula el angulo que hay entre el eje x y el vector que va del centro al inicio del arco
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


# Datos de prueba: simulación de G-code
gcode = [
    "G0 X50 Y50",   # Ir al punto inicial (sin dibujar)
    "G1 X200 Y50",  # Línea horizontal
    "G1 X200 Y200", # Línea vertical
    "G1 X50 Y200",  # Línea horizontal inversa
    "G1 X50 Y50"    # Cierre del cuadrado
]

root = tk.Tk()
root.title("Visualización de Arco G-code")
canvas = tk.Canvas(root, width=300, height=300, bg="white")
canvas.pack()

# Datos de ejemplo (G2: arco horario)
x_start, y_start = 100, 100
x_end, y_end = 150, 100
i, j = 25, 0  # centro a 25 px a la derecha (125, 100)

params = gcode_a_createarc(x_start, y_start, x_end, y_end, i, j, sentido_horario=True)

canvas.create_arc(
    params["x0"], params["y0"], params["x1"], params["y1"],
    start=params["start"],
    extent=params["extent"],
    style="arc",
    outline="red"
)
