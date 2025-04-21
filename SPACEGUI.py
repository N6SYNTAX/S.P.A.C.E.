import sys
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QOpenGLWidget
from OpenGL.GL import *
from OpenGL.GLU import *

# ------------------------------
# Globe Widget (with Earth Texture)
# ------------------------------
class GlobeWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.xRot = 0.0           # Rotation from mouse (x-axis)
        self.yRot = 0.0           # Rotation from mouse (y-axis)
        self.timeRot = 0.0        # Additional rotation from the slider (simulating 24-hour day)
        self.lastPos = QtCore.QPoint()

    def initializeGL(self):
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_TEXTURE_2D)  # Enable texture mapping (available in OpenGL 2.1 fixed-function pipeline)

        # Enable basic lighting
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glShadeModel(GL_SMOOTH)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        light_position = [1.0, 1.0, 1.0, 0.0]
        glLightfv(GL_LIGHT0, GL_POSITION, light_position)

        # Load the Earth texture image (ensure "earth.jpg" exists in your working directory)
        self.textureID = self.loadTexture("Earth.png")

        # Create a quadric object and enable texturing
        self.quadric = gluNewQuadric()
        gluQuadricTexture(self.quadric, GL_TRUE)
        gluQuadricNormals(self.quadric, GLU_SMOOTH)

    def loadTexture(self, imagePath):
        image = QtGui.QImage(imagePath)
        if image.isNull():
            print("Failed to load texture image!")
            return 0
        # Convert image to a format suitable for OpenGL (RGBA8888)
        image = image.convertToFormat(QtGui.QImage.Format_RGBA8888)
        width = image.width()
        height = image.height()
        ptr = image.bits()
        ptr.setsize(image.byteCount())
        data = np.array(ptr).reshape(height, width, 4)

        # Generate a texture ID and upload the image data to OpenGL.
        texID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texID)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0,
                     GL_RGBA, GL_UNSIGNED_BYTE, data)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glBindTexture(GL_TEXTURE_2D, 0)
        return texID

    def resizeGL(self, width, height):
        if height == 0:
            height = 1
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, float(width) / float(height), 1.0, 100.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        # Set up the camera (eye at (0,0,5), looking at the origin)
        gluLookAt(0.0, 0.0, 5.0,
                  0.0, 0.0, 0.0,
                  0.0, 1.0, 0.0)
        # Apply rotations (mouse-derived and slider-based)
        glRotatef(self.xRot, 1.0, 0.0, 0.0)
        glRotatef(self.yRot + self.timeRot, 0.0, 1.0, 0.0)
        # Bind the texture and draw the sphere
        glBindTexture(GL_TEXTURE_2D, self.textureID)
        glColor3f(1.0, 1.0, 1.0)  # Ensure the texture's colors are not altered
        gluSphere(self.quadric, 1.0, 40, 40)
        glBindTexture(GL_TEXTURE_2D, 0)

    def mousePressEvent(self, event):
        self.lastPos = event.pos()

    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()
        if event.buttons() & QtCore.Qt.LeftButton:
            self.xRot += dy
            self.yRot += dx
            self.update()  # Request a repaint
        self.lastPos = event.pos()



# ------------------------------
# Main Window Definition
# ------------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Globe with Earth Texture and 24-Hour Rotation")
        self.setGeometry(100, 100, 800, 650)
        central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QtWidgets.QVBoxLayout(central_widget)

        # Add the OpenGL Globe widget
        self.globeWidget = GlobeWidget(central_widget)
        self.globeWidget.setMinimumSize(800, 600)
        layout.addWidget(self.globeWidget)

        # Add a horizontal slider to simulate the 24-hour rotation.
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal, central_widget)
        self.slider.setRange(0, 1440)  # Represent minutes in a day.
        self.slider.setValue(0)
        self.slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.slider.setTickInterval(60)
        layout.addWidget(self.slider)
        self.slider.valueChanged.connect(self.updateRotation)

        # Add a draggable widget (overlay)
        self.draggableWidget = DraggableWidget(central_widget)
        self.draggableWidget.move(340, 270)

    def updateRotation(self, value):
        # Each minute corresponds to 0.25° rotation (1440 minutes = 360°)
        angle = value / 4.0
        self.globeWidget.timeRot = angle
        self.globeWidget.update()


# ------------------------------
# Application Entry Point
# ------------------------------
if __name__ == '__main__':
    # Set the default surface format to use OpenGL 2.1
    # This ensures the fixed-function pipeline (including glEnable(GL_TEXTURE_2D)) is available.
    fmt = QtGui.QSurfaceFormat()
    fmt.setVersion(2, 1)
    QtGui.QSurfaceFormat.setDefaultFormat(fmt)

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
