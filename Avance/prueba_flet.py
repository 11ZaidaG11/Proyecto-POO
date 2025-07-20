# Se importa Flet para la interfaz gráfica
import flet as ft
from manual_usuario import ManualUsuario

# función para recibir la "página" (interfaz principal)
def main(pag: ft.Page):
    pag.title = "Simulador CNC"
    
    # Fuentes
    pag.fonts = { 
        "Press Start 2P": "https://raw.githubusercontent.com/google/fonts/main/ofl/pressstart2p/PressStart2P-Regular.ttf",
        "Space Mono": "https://raw.githubusercontent.com/google/fonts/main/ofl/spacemono/SpaceMono-Regular.ttf"
    }
    
    # Colores
    blue_1 = "#004aad"
    blue_2 = "#50c0ff"
    blue_3 = "#a9e0ff"
    blue_4 = "#d6f0ff"

    # Crear manual de usuario
    manual = ManualUsuario()

    # Función para abrir el manual desde el botón
    def abrir_manual(e):
        pag.dialog = manual.dialog
        manual.open(e)

    # Encabezado
    title = ft.Container(
        content=ft.Text("SIMULADOR CNC", 
                        color="white", 
                        font_family="Press Start 2P",
                        size=60
        ),
        height=130,
        bgcolor=blue_1,
        alignment=ft.alignment.center
    )

    # Campo para escribir en lenguaje natural
    natural_tf = ft.TextField(
        label="Lenguaje natural",
        bgcolor=blue_4,
        text_style=ft.TextStyle(
            size=16, 
            color="black",
            font_family="Space Mono"
        ),
        label_style=ft.TextStyle(
            size=16, 
            color=blue_1, 
            font_family="Space Mono"
        ),  
        border_color=blue_1,
        multiline=True,
        min_lines=1,
        max_lines=11,
    )

    # Crea un archivo de texto con el input de natural_tf
    def natural_file(e):
        with open("natural_file.txt", "w", encoding="utf-8") as f:
            f.write(natural_tf.value)

    traductor_but = ft.ElevatedButton(
        on_click=natural_file,
        text="Traducir",
        color="white",
        bgcolor=blue_1,
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(font_family="Space Mono")
        )
    )

    # Mostrar el G-Code generado (cuando se genere automáticamente)
    gcode_tf = ft.TextField(
        label="Código G",
        bgcolor=blue_4,
        text_style=ft.TextStyle(
            size=16, 
            color="black",
            font_family="Space Mono"
        ),
        label_style=ft.TextStyle(
            size=16, 
            color=blue_1, 
            font_family="Space Mono"
        ),  
        border_color=blue_1,
        multiline=True,
        min_lines=1,
        max_lines=11,
        value="", #! translator file value
        disabled=True
    )

    # El botón copiar copia el G-Code al portapapeles
    def copy_gcode(e):
        pag.set_clipboard(gcode_tf.value)

    copy_but = ft.ElevatedButton(
        on_click=copy_gcode,
        text="Copiar",
        color="white",
        bgcolor=blue_1,
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(font_family="Space Mono")
        )
    )

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

    # Botón de ayuda (manual)
    user_but = ft.ElevatedButton(
        text="?",
        color="white",
        bgcolor=blue_1,
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(font_family="Space Mono"),
            shape=ft.CircleBorder()
        ),
        width=40,
        height=40,
        on_click=abrir_manual
    )

    # Botón de parar
    stop_but = ft.ElevatedButton(
        text="◻",
        color="white",
        bgcolor=blue_1,
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(font_family="Space Mono"),
            shape=ft.CircleBorder()
        ),
        width=40,
        height=40  
    )

    # Campo para ingresar nombre o tipo de lámina
    sheet_tf = ft.TextField(
        label="Lamina",
        bgcolor=blue_4,
        text_style=ft.TextStyle(
            size=16, 
            color="black",
            font_family="Space Mono"
        ),
        label_style=ft.TextStyle(
            size=16, 
            color=blue_1, 
            font_family="Space Mono"
        ),  
        border_color=blue_1
    )

    # Botón de iniciar simulación
    start_but = ft.ElevatedButton(
        text="▷",
        color="white",
        bgcolor=blue_1,
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(font_family="Space Mono"),
            shape=ft.CircleBorder()
        ),
        width=40,
        height=40  
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
        content=ft.Text(""),
        bgcolor="White",
        width=1050,
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

# Ejecutar la app
ft.app(main, assets_dir="assets")
