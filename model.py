import threading
import time
import os
import pwd
import psutil

class Model:

    # Método estático para obter informações sobre a memória do sistema.
    @staticmethod
    def get_memory_info():
        info = {}
        with open('/proc/meminfo') as meminfo_file:
            for line in meminfo_file:
                parts = line.split(':') # separando chaves e valores
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip().split()[0]
                    info[key] = value

        return info

    # Métodos para dados da memória
    def get_memory_percent_used(self):
        data = self.get_memory_info() # buscando os dados de proc/meminfo

        # Calculo da memória usada Total - (Livre - Buffer - Cache)
        used = float(data['MemTotal']) - float(data['MemFree']) - float(data['Buffers']) - float(data['Cached'])

        mem_used = (used / 1024) / 1024 # convertendo para GB
        mem_used_percent = (used / float(data['MemTotal'])) * 100 # Calculando a % a partir do total

        percent_used = f"Memória Usada: {mem_used:.1f}GB ({mem_used_percent:.2f}%)"

        return percent_used
        
    def get_memory_percent_free(self):
        data = self.get_memory_info()
        mem_free = (float(data['MemFree']) / 1024) / 1024
        percent_free = (float(data['MemFree']) / float(data['MemTotal'])) * 100
        final_data = f"Memória Livre: {mem_free:.1f}GB ({percent_free:.2f}%)"
        return final_data

    def get_memory_total_RAM(self):
        data = self.get_memory_info()
        memTotal = (float(data['MemTotal']) / 1024) / 1024
        final_data = f'Memória Física: {memTotal:.1f} GB'

        return final_data

    def get_memory_total_virtual(self):
        data = self.get_memory_info()
        vmTotal = (float(data['VmallocTotal']) / 1024) / 1024
        final_data = "Memória Virtual: " + str(int(vmTotal)) + 'GB'

        return final_data

    # Método para obter o total de memória usado em buffers e cache
    def get_memory_buffer_cache(self):
        data = self.get_memory_info()
        bf = float(data['Buffers']) + float(data['Cached'])
        buffer_cache = (bf / 1024) / 1024
        percent_bf = (bf / float(data['MemTotal'])) * 100
        final_data = f"Buffer/cache {buffer_cache:.1f}GB ({percent_bf:.2f}%)"

        return final_data


    # Método para obter o dados de CPU.
    def get_cpu_usage(self):
        total_time = 0
        with open('/proc/stat') as f:
            line = f.readline()
            parts = line.split()
            total_time = sum(map(int, parts[1:]))
            idle_time = int(parts[4])
        return 100 - ((idle_time / total_time) * 100)

    def get_cpu_idle_time(self):
        return 100 - self.get_cpu_usage()

    def get_total_processes(self):
        process_count = 0
        for _, dirs, _ in os.walk('/proc'):
            for dir in dirs:
                if dir.isdigit():
                    process_count += 1
        return process_count

    # Método para contar o total de threads
    def get_total_threads(self):
        thread_count = 0
        for pid in os.listdir('/proc'):
            if pid.isdigit():
                try:
                    with open(f'/proc/{pid}/status') as f:
                        for line in f:
                            if 'Threads' in line:
                                thread_count += int(line.split()[1])
                                break
                except FileNotFoundError:
                    pass
        return thread_count

    # Método para obter a lista de processos
    def get_processes(self):
        processes = []

        for pid in os.listdir('/proc'):
            if pid.isdigit():
                try:
                    with open(f'/proc/{pid}/status') as f:
                        name = ''
                        user = ''
                        vmPeak = ''
                        vmSize = ''
                        vmExe = ''
                        vmStk = ''
                        for line in f:
                            if 'Name' in line:
                                name = line.split()[1]
                            elif 'Uid' in line:
                                uid = line.split()[1]
                                user = pwd.getpwuid(int(uid)).pw_name

                        processes.append((int(pid), name, user))
                        
                except FileNotFoundError:
                    pass
        return processes

     # Método para obter a lista de threads de um processo.
    def get_threads(self, pid):
        threads = []
        try:
            with open(f'/proc/{pid}/status') as f:
                for line in f:
                    if 'Threads' in line:
                        threads.append(int(line.split()[1]))
                        break
        except FileNotFoundError:
            pass
        return threads

    # Obter os detalhes de um processo
    def get_process_details(self, pid):
        data = self.get_memory_info()
        MemTotal = float(data['MemTotal'])

        details = {
            'Name': '',
            'State': '',
            'Memória Alocada': '0',
            'Páginas (total)': '0',
            'Páginas (de Código)': '0',
            'Páginas (Stack)': '0',
            'Uptime': '',
            'Priority': '',
            'Nice': '',
            'Uso da Memória': '',
            'VmPeak': '0',
            'VmSize': '0',
            'VmExe': '0',
            'VmStk': '0',
            'Threads': '0',
        }
        try:
            with open(f'/proc/{pid}/status') as f:
                for line in f:
                    if 'Name' in line:
                        details['Name'] = line.split()[1]
                    elif 'State' in line:
                        details['State'] = line.split(':', 1)[1].strip()
                    elif 'VmPeak' in line:
                        vmPeak = line.split()[1]
                        details['VmPeak'] = vmPeak + 'KB'
                        details['Memória Alocada'] = vmPeak + 'KB'
                    elif 'VmSize' in line:
                        vmSize = line.split()[1]
                        details['VmSize'] = vmSize + 'KB'
                        details['Páginas (total)'] = int(int(vmSize) / (4 * 1024)) # divisão por 4KB (4 * 1024)
                    elif 'VmExe' in line:
                        vmExe = line.split()[1]
                        details['VmExe'] = vmExe + 'KB'
                        details['Páginas (de Código)'] = int(vmExe) / (4 * 1024)
                    elif 'VmStk' in line:
                        vmStk = line.split()[1]
                        details['VmStk'] = vmStk + 'KB'
                        details['Páginas (Stack)'] = int(vmStk) / (4 * 1024)
                    elif 'Threads' in line:
                        details['Threads'] = line.split()[1]
                    elif 'VmRSS' in line:
                        vmRSS = line.split()[1]
                        details['Uso da Memória'] = f'{(float(vmRSS) / MemTotal) * 100:.2f}%'
        except FileNotFoundError:
            pass

        try:
            with open(f'/proc/{pid}/stat') as f:
                data = f.read().split()
                print(data)
                details['Uptime'] = float(data[13]) / 100  # Converter para segundos
                details['Priority'] = int(data[17])
                details['Nice'] = int(data[18])

        except FileNotFoundError:
            pass
        # obter uso da cpu por processo 
        processo = psutil.Process(pid)
        uso_cpu = processo.cpu_percent()
        details['Uso da CPU'] = f'{uso_cpu}%'
        return details
