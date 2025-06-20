import flet as ft

def main(pag: ft.Page):
    pag.title = "Simulador CNC"
    
    pag.fonts = { 
        "Press Start 2P": "https://raw.githubusercontent.com/google/fonts/main/ofl/pressstart2p/PressStart2P-Regular.ttf",
        "Space Mono": "https://raw.githubusercontent.com/google/fonts/main/ofl/spacemono/SpaceMono-Regular.ttf"
    }
    # Colores
    blue_1 = "#004aad"
    blue_4 = "#d6f0ff"

    title = ft.Container(
        content=ft.Text("Simulador CNC", 
                        color="white", 
                        font_family="Press Start 2P",
                        size=40
        ),
        height=150,
        bgcolor=blue_1,
        alignment=ft.alignment.center,
    )

    natural_tf = ft.TextField(
        label="Lenguaje natural",
        text_style=ft.TextStyle(size=16, color="black", font_family="Space Mono"),
        label_style=ft.TextStyle(size=14, color=blue_1, font_family="Space Mono"),  
        multiline=True,
        min_lines=1,
        max_lines=10,
    )

    traductor_zone = ft.Container(
        content=natural_tf,
        width=550,
        bgcolor=blue_4,

    )

    pag.add(
        title, traductor_zone
    )

ft.app(main, assets_dir="assets")
