from model import Model
from view import View
import threading

class Controller:

    def __init__(self, model, view):
        self.model = model
        self.view = view

        # inciando thread de atualização das informações
        self.controller_thread = threading.Thread(target=self.run_threaded_functions)
        self.controller_thread.start()

    #funções que serão executadas no loop
    def run_threaded_functions(self):
        self.update_system_info()
        self.update_memory_info()
        self.update_graph_info()

    def update_system_info(self):
        # Uso de CPU
        cpu_usage = self.model.get_cpu_usage()
        self.view.display_cpu_usage(cpu_usage)

        # Tempo ocioso de CPU
        cpu_idle_time = self.model.get_cpu_idle_time()
        self.view.display_cpu_idle_time(cpu_idle_time)

        # Total de processos
        total_processes = self.model.get_total_processes()
        self.view.display_total_processes(total_processes)

        # Total de threads
        total_threads = self.model.get_total_threads()
        self.view.display_total_threads(total_threads)

        # Exibição dos processos
        processes = self.model.get_processes()
        self.view.display_processes(processes)

    def update_memory_info(self):
        mem_percent_used = self.model.get_memory_percent_used()
        mem_percent_free = self.model.get_memory_percent_free()
        mem_total_ram = self.model.get_memory_total_RAM()
        mem_total_virtual = self.model.get_memory_total_virtual()
        mem_cached_buffer = self.model.get_memory_buffer_cache()

        self.view.display_memory_used(mem_percent_used)
        self.view.display_memory_free(mem_percent_free)
        self.view.display_total_ram(mem_total_ram)
        self.view.display_total_virtual(mem_total_virtual)
        self.view.display_buffercache(mem_cached_buffer)

    def update_graph_info(self):
        self.view.update_cpu_usage_graph()
        self.view.update_memory_pie_chart()
        self.view.update_processes_threads_bar_chart()

    def get_process_details(self, pid):
        return self.model.get_process_details(pid)
