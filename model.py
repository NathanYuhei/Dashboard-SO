import threading
import time
import subprocess

# FEITO Atualizar em intervalos regulares de tempo, 5 sec

# TODO Mostrar informações globais do sistema
# TODO Mostrar informações individualizadas por processo
# TODO Software multitarefa (threads)
# TODO Utilizar o padrão MVC


class Model:

    """
    @staticmethod
    def getCpuInfo():
        info = {}
        with open('/proc/cpuinfo') as meminfo_file:
            for line in meminfo_file:
                parts = line.split(':')
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip().split()[0]
                    info[key] = value
        return info

        """

    @staticmethod
    def get_memory_info():
        info = {}
        with open('/proc/meminfo') as meminfo_file:
            for line in meminfo_file:
                parts = line.split(':')
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip().split()[0]
                    info[key] = value

        return info

    def get_memory_percent_used(self):
        data = self.get_memory_info()
        mem_used_percent = ((float(data['MemTotal']) - float(data['MemFree'])) / float(data['MemTotal'])) * 100

        percent_used = "Memória Usada: " + str(int(mem_used_percent)) + '%'

        return percent_used

    def get_memory_percent_free(self):
        data = self.get_memory_info()
        percent_free = int((float(data['MemFree']) / float(data['MemTotal'])) * 100)
        final_data = "Memória Livre: " + str(percent_free) + '%'
        return final_data

    def get_memory_total_RAM(self):
        data = self.get_memory_info()
        memTotal = (float(data['MemTotal']) / 1024) / 1024
        final_data = 'Memória Física: ' + str(int(memTotal)) + 'GB'

        return final_data

    def get_memory_total_virtual(self):
        data = self.get_memory_info()
        vmTotal = (float(data['VmallocTotal']) / 1024) / 1024
        final_data = "Memória Virtual: " + str(int(vmTotal)) + 'GB'

        return final_data

    def get_cpu_usage(self):
        result = subprocess.run(["mpstat", "1", "1"], capture_output=True, text=True)
        if result.returncode == 0:
            lines = result.stdout.splitlines()
            for line in lines:
                if "all" in line:
                    usage = line.split()[-1]
                    usage = usage.replace(',', '.')  # Substitui vírgula por ponto
                    return float(usage)
        return 0.0

    def get_cpu_idle_time(self):
        return 100 - self.get_cpu_usage()

    def get_total_processes(self):
        result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
        return len(result.stdout.split('\n')) - 1

    def get_total_threads(self):
        result = subprocess.run(["ps", "-eT"], capture_output=True, text=True)
        return len(result.stdout.split('\n')) - 1

    def get_processes(self):
        result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
        processes = []
        for line in result.stdout.split('\n')[1:-1]:
            columns = line.split()
            pid = int(columns[1])
            user = columns[0]
            name = columns[10]
            processes.append((pid, name, user))
        return processes

    def get_threads(self, pid):
        result = subprocess.run(["ps", "-eT"], capture_output=True, text=True)
        threads = []
        for line in result.stdout.split('\n')[1:-1]:
            columns = line.split()
            if int(columns[0]) == pid:
                thread_id = int(columns[1])
                user_time = columns[2]
                system_time = columns[3]
                threads.append((thread_id, user_time, system_time))
        return threads

    def get_process_details(self, pid):
        result = subprocess.run(["ps", "-p", str(pid), "-o", "%cpu,%mem,cmd"], capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            return f"Não foi possível obter detalhes para o processo com PID {pid}"