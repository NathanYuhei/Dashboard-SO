
import time
import tkinter as tk

from controller import Controller
from model import Model
from view import View

if __name__ == "__main__":
    root = tk.Tk()
    model = Model()
    view = View(root)
    controller = Controller(model, view)
    view.set_controller(controller)  # Define o controlador na instância da View

    def update():
        controller.update_system_info()
        root.after(5000, update)


    update()
    root.mainloop()