from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QTimer

class AssistantWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.resize(180, 180)

        self.label = QLabel(self)
        self.label.setGeometry(0, 0, 180, 180)

        self.text = QLabel(self)
        self.text.setGeometry(10, 150, 160, 30)
        self.text.setStyleSheet("color:white;font-size:12px;")

        self.states = {
            "idle": QPixmap("assets/zarya_idle.png"),
            "listening": QPixmap("assets/zarya_listening.png"),
            "thinking": QPixmap("assets/zarya_thinking.png"),
            "talking": QPixmap("assets/zarya_talking.png")
        }

        self.set_state("idle")
        self.move_to_corner()
        self.blink_timer = QTimer()
        self.blink_timer.timeout.connect(self.idle_animation)
        self.blink_timer.start(3000)

    def move_to_corner(self):
        screen = self.screen().availableGeometry()
        x = screen.width() - 200
        y = screen.height() - 200
        self.move(x, y)

    def set_state(self, state):
        self.label.setPixmap(self.states[state])
        self.label.setScaledContents(True)

    def say(self, text):
        self.text.setText(text)

    def idle_animation(self):
        self.set_state("idle")