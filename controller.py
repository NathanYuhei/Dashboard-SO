from model import Model
from view import View


class Controller:

    """
    def run(self):
        memory_info = Model.getMemoryInfo()
        View.printMemoryInfo(memory_info)
    """

    def __init__(self, model, view):
        self.model = model
        self.view = view

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

        # Exibição dos threads de cada processo
        for pid, _, _ in processes:
            threads = self.model.get_threads(pid)
            self.view.display_total_threads(threads)