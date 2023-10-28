
import time
import tkinter as tk

from controller import Controller
from model import Model
from view import View

if __name__ == "__main__":

    def update():
        controller.update_system_info()
        controller.update_memory_info()
        root.after(5000, update)


    root = tk.Tk()

    model = Model()
    view = View(root)
    controller = Controller(model, view)

    view.set_controller(controller)  # Define o controlador na instância da View
    update()

    view.run()
