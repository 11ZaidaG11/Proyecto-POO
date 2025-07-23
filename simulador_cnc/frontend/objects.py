import flet as ft

# Colores
blue_1 = "#004aad"
blue_2 = "#50c0ff"
blue_3 = "#a9e0ff"
blue_4 = "#d6f0ff"
font = "Space Mono"

class TextField(ft.TextField): # Campos de texto
    def __init__(self, label: str, rd: bool = False):
        super().__init__( # Hereda de TextField e inicializa
            label = label,
            read_only = rd,
            text_style = ft.TextStyle(
                size = 16,
                color = "black",
                font_family = font
            ),
            label_style = ft.TextStyle(
                size = 16, 
                color = blue_1, 
                font_family = font
            ),
            bgcolor = blue_4,
            border_color = blue_1,
            multiline = True,
            min_lines = 1,
            max_lines = 11,
        )

class CircularButt(ft.ElevatedButton):
    def __init__(self, text: str, on_click: callable):
        super().__init__(
            text = text,
            on_click = on_click,
            width = 40,
            height = 40,
            color = "white",
            bgcolor = blue_1,
            style = ft.ButtonStyle(
                text_style = ft.TextStyle(font_family = font),
                shape = ft.CircleBorder()
            )
        )

class Button(ft.ElevatedButton):
    def __init__(self, text: str, on_click: callable):
        super().__init__(
            text = text,
            on_click = on_click,
            color = "white",
            bgcolor = blue_1,
            style = ft.ButtonStyle(
                text_style = ft.TextStyle(font_family = font)
            )
        )