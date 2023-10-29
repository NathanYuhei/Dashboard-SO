
import time
import tkinter as tk
import threading

from controller import Controller
from model import Model
from view import View

if __name__ == "__main__":

    def update():
        controller.update_system_info()
        controller.update_memory_info()
        controller.update_graph_info()
        root.after(5000, update)


    root = tk.Tk()

    model = Model()
    view = View(root)
    controller = Controller(model, view)

    #thread para atualizar os dados
    update_thread = threading.Thread(target=update)
    update_thread.start()

    view.set_controller(controller)  # Define o controlador na instância da View
    update()

    view.run()
