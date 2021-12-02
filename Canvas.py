from TensorBlock import TensorBlock
from PyQt5 import QtGui,QtCore, QtWidgets
import numpy as np

class Canvas(QtWidgets.QWidget):

    DELTA = 10 #for the minimum distance        

    def __init__(self, parent):
        super(Canvas, self).__init__(parent)
        self.draggin_idx = -1        
        self.setGeometry(0,0,400,400)
        #self.points = np.array([[v*5,v*5] for v in range(75)], dtype=np.float)

        self.block = TensorBlock("Test",self)
        self.block.move(200,200)
        self.block.resize(50,50)

        self.widgets = [ self.block ]

        self.points = [ (i*10,i*10) for i in range(50) ]

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawPoints(qp)
        self.update()
        qp.end()

    def drawPoints(self, qp):
        point_pen = QtGui.QPen(QtCore.Qt.red)
        point_pen.setWidth(4)
        line_pen = QtGui.QPen(QtCore.Qt.black)
        line_pen.setWidth(1)
        qp.setPen(point_pen)

        for w in self.widgets:
            if isinstance(w, TensorBlock):
                cx, cy = w._center()
                for x,y in w.drawable_points():
                    qp.setPen(line_pen)
                    qp.drawLine(x,y,cx,cy)
                    qp.setPen(point_pen)
                    qp.drawPoint(x,y)
                    #print(x,", ",y)

    def _get_point(self, evt):
        return np.array([evt.pos().x(),evt.pos().y()])

    def _inside(self, point):
        x,y = point
        for i in range(len(self.widgets)):
            w = self.widgets[i]
            if x >= w.x() and x <= (w.x()+w.width()) and y >= w.y() and y <= (w.y()+w.height()):
                return i
        return -1

    #get the click coordinates
    def mousePressEvent(self, evt):
        if evt.button() == QtCore.Qt.LeftButton and self.draggin_idx == -1:
            point = self._get_point(evt)
            self.draggin_idx = self._inside(point)

    def mouseMoveEvent(self, evt):
        if self.draggin_idx != -1:
            point = self._get_point(evt)
            #self.points[self.draggin_idx] = point
            half_width = int( self.widgets[self.draggin_idx].width()/2 )
            half_height = int( self.widgets[self.draggin_idx].height()/2 )
            self.widgets[self.draggin_idx].move( point[0]-half_width, point[1]-half_height )
            #self.widgets[self.draggin_idx].move( point[0], point[1] )
            self.update()

    def mouseReleaseEvent(self, evt):
        if evt.button() == QtCore.Qt.LeftButton and self.draggin_idx != -1:
            point = self._get_point(evt)
            #self.points[self.draggin_idx] = point
            #self.widgets[self.draggin_idx].move( point[0], point[1] )
            half_width = int( self.widgets[self.draggin_idx].width()/2 )
            half_height = int( self.widgets[self.draggin_idx].height()/2 )
            self.widgets[self.draggin_idx].move( point[0]-half_width, point[1]-half_height )
            self.draggin_idx = -1
            self.update()
