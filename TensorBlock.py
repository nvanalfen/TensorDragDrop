from PyQt5 import QtGui,QtCore, QtWidgets
import numpy as np

class TensorBlock(QtWidgets.QLabel):

    def __init__(self, label, upper):
        super().__init__(label, upper)
        self.canvas = upper
        self.setStyleSheet("""background-color: white;
                           border: 1px solid black;""")
        self.setAlignment(QtCore.Qt.AlignCenter)

        print(self.x())
        print(self.height())

        # 4-tuple, points represent (x, y, left(-1) or N/A(0) or right(1), above(-1) or N/A(0) or below(1))
        self.points = [(-50, 0)]
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

        for x,y in self.points:
            new_x = cx + x
            new_y = cy + y

            pts.append( (new_x, new_y) )

        return pts

    def drawPoints(self, qp):
        point_pen = QtGui.QPen(QtCore.Qt.red)
        point_pen.setWidth(4)
        line_pen = QtGui.QPen(QtCore.Qt.black)
        line_pen.setWidth(1)
        qp.setPen(point_pen)

        cx, cy = self._center()
        for x,y in self.drawable_points():
            qp.setPen(line_pen)
            qp.drawLine(x,y,cx,cy)
            qp.setPen(point_pen)
            qp.drawPoint(x,y)
