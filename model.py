import threading
import time
# TODO Atualizar em intervalos regulares de tempo, 5 sec
# TODO Mostrar informações globais do sistema
# TODO Mostrar informações individualizadas por processo
# TODO Software multitarefa (threads)
# TODO Utilizar o padrão MVC


class Model:

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
