import flet as ft

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
    )

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

    # Cuadro de texto emergente
    user_manual = ft.AlertDialog(
        title=ft.Text(
            "Manual de usuario",
            font_family="Space Mono"
        ),
        title_padding=ft.padding.only(20, 20, 20, 0), # Espacio alrededor del titulo
        content=ft.Container(
            width=600,
            content=ft.Text(
                "Un manual de usuario es un documento que proporciona instrucciones" \
                " y orientación a los usuarios para el uso adecuado de un producto," \
                "sistema o servicio.",
                font_family="Space Mono",
                text_align=ft.TextAlign.JUSTIFY, # Justicar el texto
            ),
        ),
    )

    user_but = ft.ElevatedButton(
        on_click=lambda e: pag.open(user_manual), # Acción del boton
        text="?",
        color="white",
        bgcolor=blue_1,
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(font_family="Space Mono"),
            shape=ft.CircleBorder()
        ),
        width=40,
        height=40    
    )

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

    draw_zone = ft.Container(
        content=ft.Text(""),
        bgcolor="White",
        width=1050,
        expand=True
    )

    simul_zone = ft.Container(
        content=ft.Column(
            controls=[tool_zone, draw_zone]
        ),
        expand=True
    )

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

ft.app(main, assets_dir="assets")
