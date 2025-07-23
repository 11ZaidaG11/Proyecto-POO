import flet as ft
<<<<<<< HEAD
import asyncio
from backend.actions import natural_file, copy_gcode, graficar, vaciar
from frontend.objects import TextField, CircularButt
from backend.modulo1 import ManualUsuario
from backend.actions import natural_file, copy_gcode
=======
from backend.actions import natural_file, copy_gcode, graficar
>>>>>>> 43c7fc2f9a9aeb882995d75329377dbebe45ca18
from frontend.objects import TextField, CircularButt, Button
from frontend.manual_usuario import ManualUsuario

# Interfaz principal
def mai(pag: ft.Page):

    # Colores
    blue_1 = "#004aad"
    blue_2 = "#50c0ff"
    blue_3 = "#a9e0ff"
    blue_4 = "#d6f0ff"

<<<<<<< HEAD
    # Crear manual de usuario
    manual = ManualUsuario(pag)

=======
>>>>>>> 43c7fc2f9a9aeb882995d75329377dbebe45ca18
    # Encabezado
    title = ft.Container(
        content = ft.Text("SIMULADOR CNC", 
                          color = "white", 
                          font_family = "Press Start 2P",
                          size = 60
        ),
        height = 130,
        bgcolor = blue_1,
        alignment = ft.alignment.center
    )

    # Instancias de clases de objects

    # Campos de texto
    natural_tf = TextField("Lenguaje Natural", False) # Ingresar lenguaje natural
    gcode_tf = TextField("Codigo G", True) # Ver el GCode generado
    sheet_tf = TextField("Lámina", False) # Ingresar tamaño de lámina

    # Botones 
<<<<<<< HEAD
    #vaciar
    stop_but = CircularButt(
    text="◻",
    on_click=lambda e: vaciar(e, natural_tf, gcode_tf, sheet_tf, pag)
    ) 
    user_but = CircularButt(
        text="?", 
        on_click=manual.open_manual  # ← activa el manual
    )
=======
    traductor_but = Button("Traducir", lambda e: natural_file(e, gcode_tf, natural_tf, pag)) # Traductor
    copy_but = Button("Copiar", lambda e: copy_gcode(e, gcode_tf, pag)) # Copiar al portapapeles
    stop_but = CircularButt("◻", print("Stop")) # Detener
>>>>>>> 43c7fc2f9a9aeb882995d75329377dbebe45ca18

    # Manual de usuario
    manual = ManualUsuario(pag)
    user_but = CircularButt("?", manual.open_manual)

    img = ft.Image(width=600, height=400, fit=ft.ImageFit.FIT_HEIGHT)
    start_but = CircularButt("▷", lambda e: graficar(e, img))



    traductor_zone = ft.Container(
        padding=ft.Padding(left=20, top=20, right=20, bottom=0),
        content=ft.Column(
            controls=[
                natural_tf, 
                ft.Container(content=traductor_but, alignment=ft.alignment.center_right), 
                gcode_tf,
                ft.Container(content=copy_but, alignment=ft.alignment.center_right), 
            ],
            spacing=10
        ),
        bgcolor=blue_3,
        width=700,
    )

    # Zona superior de controles
    tool_zone = ft.Container(
        content=ft.Row(
            controls=[
                sheet_tf,
                ft.Row(
                    controls=[start_but, stop_but, user_but],
                    spacing=10
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        height=85,
        width=1050,
        bgcolor=blue_2,
        padding=ft.padding.all(20)
    )

    # Espacio donde se dibuja el resultado del G-Code
    draw_zone = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(content=img, alignment=ft.alignment.center),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        bgcolor="White",
        width=1080,
        expand=True
    )

    # Zona central del simulador (lámina + botones)
    simul_zone = ft.Container(
        content=ft.Column(
            controls=[tool_zone, draw_zone]
        ),
        expand=True
    )

    # Añadir todos los componentes a la página
    pag.add(
        title, 
        ft.Row(
            expand=True,
            controls=[
                ft.Container(content=simul_zone, expand=True),
                ft.Container(content=traductor_zone, width=600),
            ]
        )
    )