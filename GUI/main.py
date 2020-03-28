from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Backend import *

if __name__ == "__main__":

    w = QApplication([])
    app = App()
    app.show()
    w.exec_()
