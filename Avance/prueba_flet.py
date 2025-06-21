import flet as ft

def main(pag: ft.Page):
    pag.title = "Simulador CNC"
    
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
        content=ft.Text("Simulador CNC", 
                        color="white", 
                        font_family="Press Start 2P",
                        size=50
        ),
        height=150,
        bgcolor=blue_1,
        alignment=ft.alignment.center,
    )

    natural_tf = ft.TextField(
        label="Lenguaje natural",
        bgcolor=blue_4,
        text_style=ft.TextStyle(size=16, color="black", font_family="Space Mono"),
        label_style=ft.TextStyle(size=16, color=blue_1, font_family="Space Mono"),  
        border_color=blue_1,
        multiline=True,
        min_lines=1,
        max_lines=11,
    )

    natural_but = ft.ElevatedButton(
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
        text_style=ft.TextStyle(size=16, color="black", font_family="Space Mono"),
        label_style=ft.TextStyle(size=16, color=blue_1, font_family="Space Mono"),  
        border_color=blue_1,
        multiline=True,
        min_lines=1,
        max_lines=11,
    )

    gcode_but = ft.ElevatedButton(
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
                ft.Container(content=natural_but, alignment=ft.alignment.center_right), 
                gcode_tf,
                ft.Container(content=gcode_but, alignment=ft.alignment.center_right), 
            ],
            spacing=10
        ),
        bgcolor=blue_3,
        width=700,
    )

    tool_zone = ft.Container(
        content=ft.Text("Herramientas"),
        height=80,
        width=850,
        bgcolor=blue_2,
    )

    draw_zone = ft.Container(
        content=ft.Text("Dibujo"),
        bgcolor="White",
        width=850,
        expand=True

    )

    simul_zone = ft.Container(
        content=ft.Column(controls=[tool_zone, draw_zone]),
    )

    pag.add(
        title, 
        ft.Row(
            expand=True,
            controls=[
                ft.Container(content=simul_zone, expand=True),
                ft.Container(content=traductor_zone, width=680),
            ]
        )
    )

ft.app(main, assets_dir="assets")
