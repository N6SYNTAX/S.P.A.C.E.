import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton
)
from PyQt5.QtCore import Qt, QTime, QTimer
from PyQt5.QtGui import QFontDatabase, QFont

class Time(QWidget):
    def __init__(self):
        super().__init__()

        # Internal time state
        self.time = QTime(0, 0, 0)

        # Widgets
        self.welc_lbl      = QLabel("Welcome to Satellite Parametric Analysis Computing Environment (S.P.A.C.E).")
        self.time_lbl      = QLabel("00:00:00")
        self.start_btn     = QPushButton("Start")
        self.stop_btn      = QPushButton("Stop")
        self.now_btn       = QPushButton("Now")
        self.midnight_btn  = QPushButton("Midnight")

        # Timer
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_time)

        # Build UI
        self.initUI()

    def initUI(self):
        self.setWindowTitle("S.P.A.C.E.")
        self.resize(1920, 1080)

        # Load custom font
        font_id = QFontDatabase.addApplicationFont("A-Space Regular Demo.otf")
        families = QFontDatabase.applicationFontFamilies(font_id)
        if families:
            base_font = QFont(families[0], 24)
        else:
            base_font = QFont("Arial", 24)
        self.welc_lbl.setFont(base_font)
        self.time_lbl.setFont(base_font)

        # Stylesheet
        self.setStyleSheet("""
            QPushButton { font-size: 20px; }
            QLabel { font-size: 32px; color: #5b5b5c; }
        """)

        # Layouts
        vbox = QVBoxLayout()
        vbox.addWidget(self.welc_lbl, alignment=Qt.AlignHCenter)
        vbox.addWidget(self.time_lbl, alignment=Qt.AlignHCenter)

        hbox = QHBoxLayout()
        hbox.addWidget(self.start_btn)
        hbox.addWidget(self.stop_btn)
        hbox.addWidget(self.now_btn)
        hbox.addWidget(self.midnight_btn)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        # Connect buttons
        self.start_btn.clicked.connect(self.start)
        self.stop_btn.clicked.connect(self.stop)
        self.now_btn.clicked.connect(self.now)
        self.midnight_btn.clicked.connect(self.midnight)

        # Initialize display and start ticking
        self.now()
        self.start()

    def update_time(self):
        # Advance by one second
        self.time = self.time.addSecs(1)
        self.time_lbl.setText(self.time.toString("hh:mm:ss"))

    def start(self):
        self.timer.start()

    def stop(self):
        self.timer.stop()

    def now(self):
        # Reset to the current system time
        self.time = QTime.currentTime()
        self.time_lbl.setText(self.time.toString("hh:mm:ss"))

    def midnight(self):
        # Reset to 00:00:00 and keep ticking
        self.time = QTime(0, 0, 0)
        self.time_lbl.setText(self.time.toString("hh:mm:ss"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Time()
    window.show()
    sys.exit(app.exec_())
