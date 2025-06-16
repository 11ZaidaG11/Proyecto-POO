# Simulador de CNC 2D
### The Powerpuff Coders
![Logo del proyecto](Logo.jpg)

### Integrantes:  
- Andrea Alejandra Suárez Cuervo  
- Katherine Restrepo Rodríguez  
- Zaida Alejandra Guzmán Martínez  

### Contextualización
Para comprender a cabalidad el proyecto es necesario conocer de antemano que es y para que se usa el CNC y el G-CODE.

El CNC (Control Numérico por Computadora) es un sistema que permite controlar con precisión la posición y el movimiento de elementos físicos mediante instrucciones codificadas. Este sistema se utiliza principalmente en procesos de mecanizado, como para controlar tornos CNC, fresadoras CNC o cortadoras láser, con el fin de fabricar piezas de manera eficiente y personalizada.

Para que la máquina entienda qué acción debe ejecutar, se utiliza un lenguaje de programación llamado G-Code. Este lenguaje está compuesto por una serie de instrucciones estructuradas, está compuesto por comandos G (de movimiento) y comandos M (de funciones auxiliares). Estas acciones pueden incluir desplazamientos, cortes, perforaciones, entre otros.
Cada línea de G-Code representa una orden específica y el conjunto de estas en un programa permite que la máquina realice el proceso completo de fabricación de una pieza. 

## ¿Qué hace el proyecto?
![](3.jpg)

### G-code a lenguaje natural
| **Comando** | **Ejemplo** | **Significado** | **Palabra natural** | **Ejemplo** |
| --- | --- | --- | --- | --- |
| G00 | `G00 X5 Y12` | Posicionamiento rápido: Ubicar herramienta, sin corte. | Ubicar | Ubicar en: 5, 12 |
| G01 | `G01 X6 Y8 Z-1`   | Interpolación lineal: Corte de material en línea recta. | Línea recta | Línea recta: 6, 8 |
| G02 | `G02 X10 Y7 I0 J-5` | Interpolación circular en sentido horario (Corte). | Arco horario, centro | Arco horario: 10, 7; Centro: 0, -5  |
| G03 | `G02 X4 Y9 I-10 J3` | Interpolación circular en sentido antihorario (Corte). | Arco antihorario, centro | Arco antihorario: 4, 9; Centro: 0, -5  |  

Para G02, G03 las coordenadas I(eje x) y J(eje y) indican la posición del centro de la interpolación circular, estas son relativas al punto en el que se encuentre la herramienta de corte que se comporta como un nuevo (0, 0). Como el programa pretende facilitar la experiencia de usuario I, J se recibirán con respecto al origen así como todas las demás coordenadas.

### Interfaz gráfica de usuario (GUI)
Decidimos utilizar la biblioteca estandar de interfaces graficas de pyhton, Tkinter, para relizar la interfaz grafica del simulador.  
![](1.jpg)

- **Interpolación lineal:** `canvas.create_line(x1, y1, x2, y2, fill="color")`  
El tercer y cuarto argumento x2, y2 en G-code corresponden a X, Y respectivamente ya que son la coordenada de posición final.  
- **Interpolación circular:** `canvas.create_arc(x0, y0, x1, y1,start=n,extent=n,style=tk.ARC)`  
Los primeros cuatro argumentos x0, y0, x1, y1 representan las esquinas opuestas del rectangulo que delimita la elipse o circulo de donde se extrae el arco, en G-code X e Y darian el punto final del arco e I y J se utilizarian para calcular el centro. Como se muestra en la siguiente funcion:
```python
import tkinter as tk
import math

def gcode_a_createarc(x_inicial, y_inicial, x_final, y_final, i, j, sentido_horario=True):
    # Centro del circulo
    cx=x_inicial+i
    cy=y_inicial+j
    radio=math.hypot(i,j)

    # Vertices del rectangulo
    x0 = cx - radio
    y0 = cy - radio
    x1 = cx + radio
    y1 = cy + radio

    # Angulo que hay entre el eje x y el vector que va del centro al inicio del arco
    angulo_inicial = math.degrees(math.atan2(y_inicial - cy, x_inicial - cx)) % 360

    # Angulo que hay entre el eje x y el vector que va del centro al final del arco
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

```
  
## Presentación del Diagrama de Clases

```mermaid
---
config:
  theme: default
  look: handDrawn
  layout: dagre
title: Simulador de CNC
---
classDiagram
direction TB
    class WorkArea {
	    - size: tuple[float, float, float]
    }
    class Sheet {
	    - material: str
	    - size: list[float, float, float]
	    + is_fit(area: Workarea) : bool
    }
    class NaturalFile {
	    - name: str
    }
    class Translator {
	    - dictionary: dict[natural_word: 'G-code']
	    + translate(naturalfile: NaturalFile) : GcodeFile
    }
    class GCodeFile {
	    - name: str
    }
    class ModifiedSheet {
    }
    class CNCMachine {
	    - name: str
	    - work_area: WorkArea
	    - tool: CutterTool
	    + start()
	    + activate_tool()
	    + stop()
	    + deactivate_tool()
    }
    class CutterTool {
	    + apply(sheet: Sheet, gcode: GCodeFile) : ModifiedSheet
    }

    Sheet <|-- ModifiedSheet
    CNCMachine --> WorkArea
    CNCMachine --> CutterTool
    Translator --> GCodeFile
    Translator --> NaturalFile
    CNCMachine --> Translator
    CutterTool --> Sheet
    CutterTool --> ModifiedSheet
    CutterTool ..> GCodeFile : needs
```
