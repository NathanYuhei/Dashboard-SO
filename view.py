# view.py
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import re
import threading

class View:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x600")
        self.controller = None
        self.root.title("Dashboard de SO")

        self.processes_listbox = tk.Listbox(root, selectmode=tk.SINGLE,
                                            highlightcolor="light gray", relief="solid", width=40, height=30)

        self.processes_listbox.bind("<Double-Button-1>", self.show_process_details)

        self.processes_label = tk.Label(self.root, text='Processos')

        self.cpu_usage_label = tk.Label(self.root)
        self.cpu_idle_time_label = tk.Label(self.root)
        self.total_processes_label = tk.Label(self.root)
        self.total_threads_label = tk.Label(self.root)

        self.memory_used_percent_label = tk.Label(self.root)
        self.memory_free_percent_label = tk.Label(self.root)
        self.memory_total_ram_label = tk.Label(self.root)
        self.memory_total_virtual_label = tk.Label(self.root)
        self.memory_total_buffercache_label = tk.Label(self.root)

        self.cpu_usage_label.grid(row=1, column=3)
        self.cpu_idle_time_label.grid(row=2, column=3)
        self.total_processes_label.grid(row=3, column=3)
        self.total_threads_label.grid(row=4, column=3)

        self.memory_used_percent_label.grid(row=1, column=1)
        self.memory_free_percent_label.grid(row=2, column=1)
        self.memory_total_buffercache_label.grid(row=3, column=1)
        self.memory_total_ram_label.grid(row=4, column=1)
        self.memory_total_virtual_label.grid(row=5, column=1)

        self.processes_label.grid(row=0, column=0)
        self.processes_listbox.grid(row=1, column=0, rowspan=6)

        #incializando thread para gráfico
        #self.graph_thread = threading.Thread(target=self.create_graph, args=(self.root,))
        #self.graph_thread.start()

        #grafico uso da CPU ao longo do tempo
        self.cpu_fig, self.cpu_ax = plt.subplots(figsize=(5, 4))
        self.cpu_line, = self.cpu_ax.plot([], [], label="Uso da CPU")
        self.cpu_canvas = FigureCanvasTkAgg(self.cpu_fig, master=self.root)
        self.cpu_canvas.get_tk_widget().grid(row=0, column=4, rowspan=6)
        self.cpu_data_history = []

        # Gráfico de pizza para uso da memória
        self.memory_fig, self.memory_ax = plt.subplots(figsize=(5, 4))
        self.memory_ax.set_title("Uso da Memória")
        self.memory_canvas = FigureCanvasTkAgg(self.memory_fig, master=self.root)
        self.memory_canvas.get_tk_widget().grid(row=6, column=4, rowspan=6)

        # Gráfico de barras para processos vs. threads
        self.processes_threads_fig, self.processes_threads_ax = plt.subplots(figsize=(5, 4))
        self.processes_threads_ax.set_title("Processos vs. Threads")
        self.processes_threads_canvas = FigureCanvasTkAgg(self.processes_threads_fig, master=self.root)
        self.processes_threads_canvas.get_tk_widget().grid(row=0, column=5, rowspan=6)

    def set_controller(self, controller):
        self.controller = controller

    def display_cpu_usage(self, usage):
        self.cpu_usage_label.config(text=f"Uso do CPU: {usage:.1f}%")

    def display_cpu_idle_time(self, idle_time):
        self.cpu_idle_time_label.config(text=f"Tempo ocioso do CPU: {idle_time:.1f}%")

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
            details_window.geometry('400x500')
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

    def display_buffercache(self, buffercache):
        self.memory_total_buffercache_label.config(text=f"{buffercache}")

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

    def create_cpu_usage_graph(self, window):
        fig = Figure(figsize=(5, 4), dpi=100)
        plot = fig.add_subplot(111)
        plot.set_title("Uso da CPU ao Longo do Tempo")
        plot.set_xlabel("Tempo")
        plot.set_ylabel("Uso da CPU (%)")
        line, = plot.plot([], [], marker='o')

        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=0, column=2)

        x_data = []  # para armazenar pontos de tempo
        y_data = []  # para armazenar dados de uso da CPU

        def update_graph():
            y_value = self.controller.model.get_cpu_usage()
            y_data = []
            y_data.append(y_value)
            x_data.append(len(y_data))

            line.set_data(x_data, y_data)
            plot.relim()
            plot.autoscale_view()
            canvas.draw()
            window.after(5000, update_graph)

        update_graph()

    # grafico de memoria usada/livre
    def create_memory_pie_chart(self, window):
        fig = Figure(figsize=(5, 4), dpi=100)
        plot = fig.add_subplot(111)

        labels = ["Usada", "Livre"]
        sizes = [float(self.controller.model.get_memory_percent_used().split('%')[0]),
                 float(self.controller.model.get_memory_percent_free().split('%')[0])]

        plot.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)

        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=0, column=3)

    # grafico de total de processos e threads
    def create_processes_threads_bar_chart(self, window):
        fig = Figure(figsize=(5, 4), dpi=100)
        plot = fig.add_subplot(111)

        labels = ["Processos", "Threads"]
        sizes = [self.controller.model.get_total_processes(), self.controller.model.get_total_threads()]

        plot.bar(labels, sizes)

        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=0, column=4)

    def update_cpu_usage_graph(self):
        # Obtenha o uso atual da CPU
        current_cpu_usage = self.controller.model.get_cpu_usage()

        # Adicione o uso atual ao histórico
        self.cpu_data_history.append(current_cpu_usage)

        # Atualize o gráfico
        self.cpu_line.set_ydata(self.cpu_data_history)
        self.cpu_line.set_xdata(range(len(self.cpu_data_history)))

        # Ajuste os limites do gráfico
        self.cpu_ax.set_xlim(0, len(self.cpu_data_history))
        self.cpu_ax.set_ylim(0, 100)  # Assumindo que é uma porcentagem

        self.cpu_ax.set_title('Uso da CPU ao longo do tempo')

        # Redesenhe o gráfico
        self.cpu_canvas.draw()

    def update_memory_pie_chart(self):

        def extract_number(s):
            return float(re.search(r'(\d+\.?\d*)', s).group(1))

        # Obtenha os dados da memória
        mem_used_str = self.controller.model.get_memory_percent_used()
        mem_free_str = self.controller.model.get_memory_percent_free()

        mem_used = extract_number(mem_used_str)
        mem_free = extract_number(mem_free_str)

        # Dados para o gráfico de pizza
        memory_data = [mem_used, mem_free]
        labels = ['Used(%)', 'Free(%)']
        colors = ['red', 'green']

        # Limpar o gráfico anterior (se existir)
        self.memory_ax.clear()

        # Atualizar o gráfico de pizza
        self.memory_ax.pie(memory_data, labels=labels, colors=colors, autopct='%1.1f%%')
        self.memory_ax.set_title('Memória livre vs utilizada (%)')

        # Redesenhe o gráfico
        self.memory_canvas.draw()

    def update_processes_threads_bar_chart(self):
        # Obtenha os dados
        total_processes = self.controller.model.get_total_processes()
        total_threads = self.controller.model.get_total_threads()

        # Dados para o gráfico de barras
        bar_data = [total_processes, total_threads]
        labels = ['Processes', 'Threads']

        # Limpar o gráfico anterior (se existir)
        self.processes_threads_ax.clear()

        # Atualizar o gráfico de barras
        self.processes_threads_ax.bar(labels, bar_data, color=['blue', 'purple'])

        # Ajustes no gráfico
        self.processes_threads_ax.set_title("Processos vs. Threads")
        self.processes_threads_ax.set_ylabel("Número")

        # Redesenhe o gráfico
        self.processes_threads_canvas.draw()