# manual_usuario.py
import flet as ft
from flet import MainAxisAlignment

# Se crea una clase para encapsular todo el manual
class ManualUsuario:
    def __init__(self):
        # inicialmente está oculto
        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Manual de usuario", font_family="Space Mono"),
            title_padding=ft.padding.only(20, 20, 20, 0),
            content=ft.Container(
                width=600,
                content=ft.Text(
                    self.texto_manual(),
                    font_family="Space Mono",
                    text_align=ft.TextAlign.JUSTIFY
                ),
            ),
            actions=[
                ft.TextButton("Cerrar", on_click=self.close)
            ],
            actions_alignment=MainAxisAlignment.END
        )
    
    # Función que retorna el texto del manual
    def texto_manual(self):
        return (
            "Este software permite controlar un sistema CNC de forma remota. "
            "En el menú lateral puedes cargar un archivo G-code, visualizar su ruta de ejecución "
            "y controlar parámetros de velocidad y posición. "
            "\n\nPasos sugeridos:\n"
            "1. Carga tu archivo desde el botón 'Cargar G-code'.\n"
            "2. Verifica la vista previa de trayectorias.\n"
            "3. Usa los controles de simulación o ejecución real para iniciar el proceso.\n"
            "4. Consulta los reportes de ejecución desde la pestaña correspondiente.\n"
            "\nEste manual se irá actualizando con nuevas versiones."
        )
    
    # Función para mostrar el diálogo
    def open(self, e):
        e.control.page.dialog = self.dialog
        self.dialog.open = True
        e.control.page.update()

    # Función para cerrar el diálogo
    def close(self, e):
        self.dialog.open = False
        e.control.page.update()
