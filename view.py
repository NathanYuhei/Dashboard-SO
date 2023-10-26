import tkinter as tk
from tkinter import scrolledtext

# TODO Formatar a apresentação dos dados e exibir por interface gráfica

class View:

    """
    def printMemoryInfo(info):
        for key, value in info.items():
            print(f"{key}: {value} GB")
        return
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Informações do Sistema")

        self.cpu_usage_label = tk.Label(root, text="Uso do CPU: ")
        self.cpu_usage_label.pack()

        self.cpu_idle_time_label = tk.Label(root, text="Tempo ocioso do CPU: ")
        self.cpu_idle_time_label.pack()

        self.total_processes_label = tk.Label(root, text="Total de processos: ")
        self.total_processes_label.pack()

        self.total_threads_label = tk.Label(root, text="Total de threads: ")
        self.total_threads_label.pack()

        self.processes_text = scrolledtext.ScrolledText(root, wrap=tk.WORD)
        self.processes_text.pack()

    def display_cpu_usage(self, usage):
        self.cpu_usage_label.config(text=f"Uso do CPU: {usage}%")

    def display_cpu_idle_time(self, idle_time):
        self.cpu_idle_time_label.config(text=f"Tempo ocioso do CPU: {idle_time}%")

    def display_total_processes(self, total_processes):
        self.total_processes_label.config(text=f"Total de processos: {total_processes}")

    def display_total_threads(self, total_threads):
        self.total_threads_label.config(text=f"Total de threads: {total_threads}")

    def display_processes(self, processes):
        self.processes_text.delete(1.0, tk.END)
        self.processes_text.insert(tk.INSERT, "Lista de processos:\n")
        self.processes_text.insert(tk.INSERT, "PID\tNome\tUsuário\n")
        for pid, name, username in processes:
            self.processes_text.insert(tk.INSERT, f"{pid}\t{name}\t{username}\n")