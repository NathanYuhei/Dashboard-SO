from model import Model
from view import View

class Controller:

    def run(self):
        memory_info = Model.getMemoryInfo()
        View.printMemoryInfo(memory_info)
