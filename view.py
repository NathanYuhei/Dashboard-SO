# view.py
import tkinter as tk

class View:
    def __init__(self, root):
        self.root = root
        self.controller = None
        self.root.title("Dashboard de SO")

        self.cpu_usage_label = tk.Label(root, text="Uso do CPU: ")
        self.cpu_usage_label.pack()

        self.cpu_idle_time_label = tk.Label(root, text="Tempo ocioso do CPU: ")
        self.cpu_idle_time_label.pack()

        self.total_processes_label = tk.Label(root, text="Total de processos: ")
        self.total_processes_label.pack()

        self.total_threads_label = tk.Label(root, text="Total de threads: ")
        self.total_threads_label.pack()

        self.processes_listbox = tk.Listbox(root)
        self.processes_listbox.pack()
        self.processes_listbox.bind("<Double-Button-1>", self.show_process_details)

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
        for pid, name, _ in processes:
            self.processes_listbox.insert(tk.END, f"{pid}: {name}")

    def show_process_details(self, event):
        selected_index = self.processes_listbox.curselection()
        if selected_index:
            selected_process = self.processes_listbox.get(selected_index)
            pid = selected_process.split(":")[0]
            details = self.controller.get_process_details(pid)  # Agora pode chamar a função em Controller
            details_window = tk.Toplevel(self.root)
            details_window.title(f"Detalhes do Processo {pid}")

            details_label = tk.Label(details_window, text=details)
            details_label.pack()

    def show_memory_info(self, mem_info):
        print(mem_info)
