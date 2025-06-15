# Simulador de CNC 2D
### The Powerpuff Coders
![Logo del proyecto](Logo.jpg)


Integrantes:  
- Andrea Alejandra Suárez Cuervo  
- Katherine Restrepo Rodríguez  
- Zaida Alejandra Guzmán Martínez  

Simulador de CNC 2D  
Ideas  
- Usuario ingresa en lenguaje natural como quiere modificar la lamina.
- El programa regresa el input del usuario en GCODE.
- En pantalla se ve como queda la lamina modificada.
- ¿Modo juego? Te muestra como debe terminar la figura y tu la replicas. 

Tareas
- Como se programa en GCODE.
- Equivalentes en lenguaje natural de GCODE.
- Como mostrar figuras en GUI (Pygame, tkinter...?) y en donde es más facil hacer el proyecto.
  
### Contextualización
Para comprender a cabalidad el proyecto es necesario conocer de antemano que es y para que se usa el CNC y el G-CODE.

El CNC (Control Numérico por Computadora) es un sistema que permite controlar con precisión la posición y el movimiento de elementos físicos mediante instrucciones codificadas. Este sistema se utiliza principalmente en procesos de mecanizado, como para controlar tornos CNC, fresadoras CNC o cortadoras láser, con el fin de fabricar piezas de manera eficiente y personalizada.

Para que la máquina entienda qué acción debe ejecutar, se utiliza un lenguaje de programación llamado G-Code. Este lenguaje está compuesto por una serie de instrucciones estructuradas, está compuesto por comandos G (de movimiento) y comandos M (de funciones auxiliares). Estas acciones pueden incluir desplazamientos, cortes, perforaciones, entre otros.
Cada línea de G-Code representa una orden específica y el conjunto de estas en un programa permite que la máquina realice el proceso completo de fabricación de una pieza. 

### ¿Qué hace el proyecto?
### G-code a lenguaje natural
| **Comando** | **Ejemplo** | **Significado** | **Palabra natural** | **Ejemplo** |
| --- | --- | --- | --- | --- |
| G00 | `G00 X5 Y12` | Posicionamiento rápido: Ubicar herramienta, sin corte. | Ubicar | Ubicar en: 5, 12. |
| G01 | `G01 X6 Y8 Z-1`   | Interpolación lineal: Corte de material en línea recta. | Línea recta | Línea recta hasta: 6, 8. |
| G02 | `G02 X10 Y7 I0 J-5` | Interpolación circular en sentido horario (Corte). | Arco horario, centro | Arco horario hasta: 10, 7; Centro: 0, -5.  |
| G03 | `G02 X4 Y9 I-10 J3` | Interpolación circular en sentido antihorario (Corte). | Arco antihorario, centro | Arco antihorario hasta: 4, 9; Centro: 0, -5.  |

Decidimos utilizar la biblioteca estandar de interfaces graficas de pyhton, Tkinter, para relizar la interfaz grafica del simulador, ya que esta nos permite representar movimientos lineales y cicurlares, para esto se pretende utilizar `canvas.create_line()` y `canvas.create_arc()`
