from PyQt5 import QtGui,QtCore, QtWidgets
import numpy as np

class TensorBlock(QtWidgets.QLabel):

    def __init__(self, label, upper):
        super().__init__(label, upper)
        self.canvas = upper
        #self.setStyleSheet("border: 1px solid black;")
        self.setStyleSheet("""background-color: white;
                           border: 1px solid black;""")
        self.setAlignment(QtCore.Qt.AlignCenter)

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

class Canvas(QtWidgets.QWidget):

    DELTA = 10 #for the minimum distance        

    def __init__(self, parent):
        super(Canvas, self).__init__(parent)
        self.draggin_idx = -1        
        self.setGeometry(0,0,400,400)
        #self.points = np.array([[v*5,v*5] for v in range(75)], dtype=np.float)

        self.label = QtWidgets.QLabel("Hello",self)
        self.label.move(40, 100)
        self.label.resize(30,10)
        self.label.setStyleSheet("border: 1px solid black;")

        self.label2 = QtWidgets.QLabel("Bye",self)
        self.label2.move(40, 200)
        self.label2.resize(30,10)
        self.label2.setStyleSheet("border: 1px solid black;")

        self.block = TensorBlock("Test",self)
        self.block.move(200,200)
        self.block.resize(50,50)

        self.widgets = [ self.label, self.label2, self.block ]

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
            #dist will hold the square distance from the click to the points
            #dist = np.array([ [w.x(), w.y()] for w in self.widgets ]) - point
            #dist = dist[:,0]**2 + dist[:,1]**2
            #dist[dist>self.DELTA] = np.inf #obviate the distances above DELTA
            #print(dist)
            #if dist.min() < np.inf:
            #if dist.min() < self.DELTA:
            #    self.draggin_idx = dist.argmin()
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

app = QtWidgets.QApplication([])

c = Canvas(None)
c.show()
app.exec_()
