import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def create_graph():
    fig = Figure(figsize=(5, 4), dpi=100)
    plot = fig.add_subplot(111)
    plot.plot([1, 2, 3, 4], [1, 4, 9, 16])

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()

window = tk.Tk()
window.title("Graph in Tkinter")

create_graph()

window.mainloop()
