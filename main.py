from PyQt5 import QtGui,QtCore, QtWidgets
import numpy as np
from Canvas import Canvas


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    c = Canvas(None)
    c.show()
    app.exec_()
