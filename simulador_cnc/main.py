import flet as ft
from frontend.app import mai

def main(page: ft.Page):
    page.title = "Simulador CNC"
    
    # Fuentes
    page.fonts = {
        "Space Mono": "https://raw.githubusercontent.com/google/fonts/main/ofl/spacemono/SpaceMono-Regular.ttf",
        "Press Start 2P": "https://raw.githubusercontent.com/google/fonts/main/ofl/pressstart2p/PressStart2P-Regular.ttf"
    }
    mai(page)

ft.app(target = main, assets_dir = "assets")