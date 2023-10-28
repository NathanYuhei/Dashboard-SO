# view.py
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import re


class View:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x600")
        self.controller = None
        self.root.title("Dashboard de SO")

        self.processes_listbox = tk.Listbox(root, selectmode=tk.SINGLE,
                                            highlightcolor="light gray", relief="solid", width=40, height=30)

        self.processes_listbox.bind("<Double-Button-1>", self.show_process_details)
        # self.create_graph(root)

        self.cpu_usage_label = tk.Label(self.root)
        self.cpu_idle_time_label = tk.Label(self.root)
        self.total_processes_label = tk.Label(self.root)
        self.total_threads_label = tk.Label(self.root)

        self.memory_used_percent_label = tk.Label(self.root)
        self.memory_free_percent_label = tk.Label(self.root)
        self.memory_total_ram_label = tk.Label(self.root)
        self.memory_total_virtual_label = tk.Label(self.root)

        self.cpu_usage_label.grid(row=0, column=2)
        self.cpu_idle_time_label.grid(row=1, column=2)
        self.total_processes_label.grid(row=2, column=2)
        self.total_threads_label.grid(row=3, column=2)

        self.memory_used_percent_label.grid(row=0, column=1)
        self.memory_free_percent_label.grid(row=1, column=1)
        self.memory_total_ram_label.grid(row=2, column=1)
        self.memory_total_virtual_label.grid(row=3, column=1)

        self.processes_listbox.grid(row=0, column=0, rowspan=6)

    def set_controller(self, controller):
        self.controller = controller

    def display_cpu_usage(self, usage):
        self.cpu_usage_label.config(text=f"Uso do CPU: {usage}%")

    def display_cpu_idle_time(self, idle_time):
        self.cpu_idle_time_label.config(text=f"Tempo ocioso do CPU: {idle_time}%")

    def display_total_processes(self, total_processes):
        self.total_processes_label.config(text=f"Total de processos: {total_processes}")

    def display_total_threads(self, total_threads):
        self.total_threads_label.config(text=f"Total de threads: {total_threads}")

    def display_processes(self, processes):
        self.processes_listbox.delete(0, tk.END)

        for pid, user, name in processes:
            self.processes_listbox.insert(tk.END, f"User {name} ({pid}): {user}")

    def show_process_details(self, event):
        selected_index = self.processes_listbox.curselection()
        if selected_index:
            selected_process = self.processes_listbox.get(selected_index)
            pid = self.get_pid(selected_process)
            details = self.controller.get_process_details(pid)  # Agora pode chamar a função em Controller
            details_window = tk.Toplevel(self.root)
            details_window.geometry('400x300')
            details_window.title(f"Detalhes do Processo {pid}")

            for key, value in details.items():
                label_text = f"{key}: {value}"
                label = tk.Label(details_window, text=label_text)
                label.pack()


    def display_memory_used(self, used):
        self.memory_used_percent_label.config(text=f"{used}")

    def display_memory_free(self, free):
        self.memory_free_percent_label.config(text=f"{free}")

    def display_total_ram(self, ram):
        self.memory_total_ram_label.config(text=f"{ram}")

    def display_total_virtual(self, virtual):
        self.memory_total_virtual_label.config(text=f"{virtual}")

    def run(self):
        self.root.mainloop()

    def create_graph(self, window):
        fig = Figure(figsize=(5, 4), dpi=100)
        plot = fig.add_subplot(111)
        line, = plot.plot([], [], marker='o')  # Linha vazia inicial com marcadores

        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=0, column=1)

        def update_graph(x_data, y_data):
            line.set_data(x_data, y_data)  # Atualiza os dados da linha
            plot.relim()  # Atualiza os limites dos eixos
            plot.autoscale_view()  # Redefine a escala dos eixos
            canvas.draw()  # Redesenha o gráfico

        # Exemplo de função para fornecer novos dados
        def get_new_data():
            x_data = [1, 2, 3, 4]  # Seus próprios valores de x
            y_data = [10, 5, 12, 7]  # Seus próprios valores de y

            update_graph(x_data, y_data)

            # Agende a próxima atualização com novos dados (aqui, atualizamos a cada 5 segundos)
            window.after(5000, get_new_data)

        get_new_data()  # Inicializa a primeira atualização com dados iniciais

    @staticmethod
    def get_pid(input_string):
        match = re.search(r'\((\d+)\)', input_string)
        if match:
            num = int(match.group(1))
            return num
        else:
            return None
