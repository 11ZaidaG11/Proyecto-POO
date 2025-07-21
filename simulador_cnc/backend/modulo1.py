import re

# El archivo con instrucciones en lenguaje natural
class NaturalFile:
    name: str = "natural_file.txt"

    def __init__(self):
        self.nf_content = self.read_file()
    
    def write_file(self, text): #! natural_tf.value: str
        with open(self.name, "w", encoding="utf-8") as nf:
            nf.write(text) #! natural_tf.value
    
    def read_file(self):
        with open(self.name, "r", encoding="utf-8") as nf:
            return nf.read()
        
# El archivo con las instrucciones G-Code
class GCodeFile:
    name: str = "gcode_file.txt"
    
    def write_file(self, text: str):
        with open(self.name, "w", encoding="utf-8") as gf:
            gf.write(text)
    def read_file(self):
        with open(self.name, "r", encoding="utf-8") as gf:
            return gf.read()
        
    def __str__(self):
        return self.read_file()
    
# Herramienta de corte 
class CutterTool:
    def __init__(self, x:float, y:float):
        self.current_X = x
        self.current_y = y

# Traductor entre el lenguaje natural y el G-Code
class Translator:
    dictionary = {
        "Ubicar": "G00",
        "Recta": "G01",
        "horario": "G02",
        "antihorario": "G03"
    }

    # Expresiones regulares
    patt1 = r"(Ubicar|Recta): (-?\d+(?:\.\d+)?), (-?\d+(?:\.\d+)?)"
    patt2 = r"Arco (horario|antihorario): (-?\d+(?:\.\d+)?), (-?\d+(?:\.\d+)?); Centro: (-?\d+(?:\.\d+)?), (-?\d+(?:\.\d+)?)"

    def __init__(self, n_file: NaturalFile):
        self.content = n_file.nf_content
        self.match1 = re.finditer(self.patt1, self.content, re.MULTILINE)
        self.match2 = re.finditer(self.patt2, self.content, re.MULTILINE)

    def translate(self) -> GCodeFile:
        lines: list = []
        if self.match1:
            for m in self.match1:
                G = self.dictionary[m.group(1)]
                X = m.group(2)
                Y = m.group(3)
                line = f"{G} X{X} Y{Y}\n"
                lines.append(line)

        if self.match2:
            for m in self.match2:
                G = self.dictionary[m.group(1)]
                X = m.group(2)
                Y = m.group(3)
                preI = m.group(4)
                preJ = m.group(5)
                I = tool.current_X - float(preI)
                J = tool.current_y - float(preJ)
                line = f"{G} X{X} Y{Y} I{I} J{J}\n"
                lines.append(line)
        
        nat_to_gc = "".join(lines)
        g_file.write_file(nat_to_gc)
        return g_file

g_file = GCodeFile()
tool = CutterTool(0,0)
