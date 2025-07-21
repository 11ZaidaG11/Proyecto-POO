import flet as ft
from frontend.app import mai

def main(page: ft.Page):
    mai(page)

ft.app(target=main)
