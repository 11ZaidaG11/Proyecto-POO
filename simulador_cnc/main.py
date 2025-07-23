import flet as ft
from frontend.app import mai

def main(pag: ft.Page):
    pag.title = "Simulador CNC"
    pag.snack_bar = ft.SnackBar(content=ft.Text(""))

    # Fuentes
    pag.fonts = {
        "Space Mono": "https://raw.githubusercontent.com/google/fonts/main/ofl/spacemono/SpaceMono-Regular.ttf",
        "Press Start 2P": "https://raw.githubusercontent.com/google/fonts/main/ofl/pressstart2p/PressStart2P-Regular.ttf"
    }
    mai(pag)

ft.app(target = main, assets_dir = "assets")