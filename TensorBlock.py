from PyQt5 import QtGui,QtCore, QtWidgets
import numpy as np

class TensorBlock(QtWidgets.QLabel):

    def __init__(self, label, upper):
        super().__init__(label, upper)
        self.canvas = upper
        self.setStyleSheet("""background-color: white;
                           border: 1px solid black;""")
        self.setAlignment(QtCore.Qt.AlignCenter)

        print(self.width())
        print(self.height())

        # 4-tuple, points represent (x, y, left(-1) or N/A(0) or right(1), above(-1) or N/A(0) or below(1))
        self.points = [(10, 0, -1, 0)]
        #self.draw_points()

    def resize(self, x, y):
        super().resize(x,y)

    def move(self, x, y):
        super().move(x,y)
        #self.draw_points()

    def _center(self):
        half_width = int( self.width()/2 )
        half_height = int( self.height()/2 )
        return self.x()+half_width, self.y()+half_height

    #def paintEvent(self, e):
    #    qp = QtGui.QPainter()
    #    qp.begin(self.canvas)
    #    self.drawPoints(qp)
    #    self.update()
    #    qp.end()

    def drawable_points(self):
        cx, cy = self._center()
        hwx = int( self.width()/2 )
        hwy = int( self.height()/2 )

        pts = []

        for x,y,horizontal,vertical in self.points:
            new_x = cx + horizontal * (x + hwx)
            new_y = cy + vertical * (y + hwy)

            pts.append( (new_x, new_y) )

        return pts

    def drawPoints(self, qp):
        pen = QtGui.QPen(QtCore.Qt.red)
        pen.setWidth(3)
        qp.setPen(pen)

        for x,y in self.drawable_points():
            qp.drawPoint(x, y)
