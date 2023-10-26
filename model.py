import threading
import time
import subprocess
import os
import pwd
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

    @staticmethod
    def getMemoryInfo():
        info = {}
        with open('/proc/meminfo') as meminfo_file:
            for line in meminfo_file:
                parts = line.split(':')
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip().split()[0]
                    info[key] = (int(value) / 1024) / 1024

        return info
    """

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

    def get_processes(self):
        processes = []
        for pid in os.listdir('/proc'):
            if pid.isdigit():
                try:
                    with open(f'/proc/{pid}/status') as f:
                        name = ''
                        user = ''
                        for line in f:
                            if 'Name' in line:
                                name = line.split()[1]
                            if 'Uid' in line:
                                uid = line.split()[1]
                                user = pwd.getpwuid(int(uid)).pw_name
                        processes.append((int(pid), name, user))
                except FileNotFoundError:
                    pass
        return processes

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

    def get_process_details(self, pid):
        details = ''
        try:
            with open(f'/proc/{pid}/status') as f:
                for line in f:
                    details += line
        except FileNotFoundError:
            pass
        return details
