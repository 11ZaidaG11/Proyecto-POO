import flet as ft

class ManualUsuario:
    def __init__(self, page: ft.Page):
        self.page = page
        self.dialog = ft.AlertDialog(
            modal=True,
            shape=ft.RoundedRectangleBorder(radius=20),
            bgcolor="#d6f1ff",
            title=ft.Text(
                "Manual de Usuario",
                font_family="Press Start 2P",
                size = 20,
                weight=ft.FontWeight.BOLD,
                color = "#004aad"
            ),
            title_padding = ft.padding.only(20, 20, 20, 0),
            content=ft.Container(
                width = 600,
                height = 400,
                padding = ft.padding.all(20),
                content = ft.Column(
                    scroll = ft.ScrollMode.AUTO,
                    controls = [
                        ft.Text(
                            self.texto_manual(),
                            font_family = "Space Mono",
                            size = 16,
                            color = "black",
                            text_align = ft.TextAlign.JUSTIFY
                        )
                    ]
                )
            ),
            actions=[
                ft.TextButton(
                    "Cerrar",
                    on_click=self.close,
                    style = ft.ButtonStyle(
                        color = {"": "#004aad"},
                        padding = ft.padding.symmetric(horizontal = 20, vertical = 10),
                        text_style = ft.TextStyle(
                            font_family = "Space Mono",
                            size = 14
                        )
                    )
                )
            ],
            actions_alignment = ft.MainAxisAlignment.END
        )
        # Esta línea es CLAVE para que funcione:
        self.page.overlay.append(self.dialog)

    def texto_manual(self):
        return(
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

    def open_manual(self, e):
        print(">> ABRIENDO MANUAL")
        self.page.dialog = self.dialog
        self.dialog.open = True
        self.page.update()

    def close(self, e):
        self.dialog.open = False
        self.page.update()
