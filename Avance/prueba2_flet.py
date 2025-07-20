import flet as ft

def main(page: ft.Page):
    page.title = "Ejemplo TextField Deshabilitado"

    texto_deshabilitado = ft.TextField(
        label="Este campo está deshabilitado",
        value="No puedes editar esto",
        disabled=True
    )

    page.add(texto_deshabilitado)

ft.app(target=main)