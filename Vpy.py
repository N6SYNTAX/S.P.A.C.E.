import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton
)
from PyQt5.QtCore import Qt, QTime, QTimer
from PyQt5.QtGui import QFontDatabase, QFont
from pyqtgraph.opengl import GLViewWidget, MeshData, GLMeshItem

class TimeGlobeWidget(QWidget):
    def __init__(self):
        super().__init__()

        # — Timer & Time State —
        self.time = QTime.currentTime()
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self._tick)

        # — Widgets —
        self.welc_lbl     = QLabel("Welcome to Satellite Parametric Analysis Computing Environment (S.P.A.C.E).")
        self.time_lbl     = QLabel(self.time.toString("hh:mm:ss"))
        self.start_btn    = QPushButton("Start")
        self.stop_btn     = QPushButton("Stop")
        self.now_btn      = QPushButton("Now")
        self.midnight_btn = QPushButton("Midnight")

        # — 3D Globe (PyQtGraph) —
        self.view = GLViewWidget()
        self.view.setCameraPosition(distance=6)
        sphere_mesh = MeshData.sphere(rows=20, cols=40)
        sphere_item = GLMeshItem(
            meshdata=sphere_mesh,
            smooth=True,
            drawEdges=False,
            shader='shaded',
            color=(0.5, 0.5, 1.0, 1.0)
        )
        self.view.addItem(sphere_item)

        # — Build UI & Layout —
        self._build_ui()
        # — Start the clock —
        self.now()
        self.start()

    def _build_ui(self):
        # Load a custom font if available
        font_id = QFontDatabase.addApplicationFont("A-Space Regular Demo.otf")
        families = QFontDatabase.applicationFontFamilies(font_id)
        base_font = QFont(families[0], 24) if families else QFont("Arial", 24)
        self.welc_lbl.setFont(base_font)
        self.time_lbl.setFont(base_font)

        # Stylesheet for consistency
        self.setStyleSheet("""
            QPushButton { font-size: 20px; }
            QLabel      { font-size: 32px; color: #5b5b5c; }
        """)

        # Layout: vertical for labels & globe, horizontal for buttons
        vbox = QVBoxLayout(self)
        vbox.addWidget(self.welc_lbl, alignment=Qt.AlignHCenter)
        vbox.addWidget(self.time_lbl, alignment=Qt.AlignHCenter)

        hbox = QHBoxLayout()
        for btn in (self.start_btn, self.stop_btn, self.now_btn, self.midnight_btn):
            hbox.addWidget(btn)
        vbox.addLayout(hbox)

        vbox.addWidget(self.view, stretch=1)

        # Connect buttons
        self.start_btn.clicked.connect(self.start)
        self.stop_btn.clicked.connect(self.stop)
        self.now_btn.clicked.connect(self.now)
        self.midnight_btn.clicked.connect(self.midnight)

    def _tick(self):
        # advance by one second
        self.time = self.time.addSecs(1)
        self.time_lbl.setText(self.time.toString("hh:mm:ss"))

    def start(self):
        self.timer.start()

    def stop(self):
        self.timer.stop()

    def now(self):
        # reset to current system time
        self.time = QTime.currentTime()
        self.time_lbl.setText(self.time.toString("hh:mm:ss"))

    def midnight(self):
        # reset to 00:00:00
        self.time = QTime(0, 0, 0)
        self.time_lbl.setText(self.time.toString("hh:mm:ss"))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("S.P.A.C.E.")
        self.resize(1280, 720)
        self.setCentralWidget(TimeGlobeWidget())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
