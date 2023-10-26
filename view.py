import tkinter

# TODO Formatar a apresentação dos dados e exibir por interface gráfica

class View:

    def printMemoryInfo(info):
        for key, value in info.items():
            print(f"{key}: {value} GB")
        return