from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QTimer


class AssistantWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )

        self.setAttribute(Qt.WA_TranslucentBackground)

        self.resize(220, 220)

        self.label = QLabel(self)
        self.label.setGeometry(0, 0, 220, 220)

        self.text = QLabel(self)
        self.text.setGeometry(10, 180, 200, 30)

        self.states = {

            "idle": QPixmap("assets/zarya_idle.png"),
            "listening": QPixmap("assets/zarya_listening.png"),
            "thinking": QPixmap("assets/zarya_thinking.png"),
            "talking": QPixmap("assets/zarya_talking.png"),
            "blink": QPixmap("assets/zarya_blink.png")

        }

        self.set_state("idle")

        self.move_to_corner()

        self.blink_timer = QTimer()
        self.blink_timer.timeout.connect(self.blink)

        self.blink_timer.start(3000)

    def move_to_corner(self):

        screen = self.screen().availableGeometry()

        x = screen.width() - 230
        y = screen.height() - 230

        self.move(x, y)

    def set_state(self, state):

        self.label.setPixmap(self.states[state])
        self.label.setScaledContents(True)

    def blink(self):

        self.set_state("blink")

        QTimer.singleShot(
            200,
            lambda: self.set_state("idle")
        )
    
    def mousePressEvent(self, event):

        self.drag_position = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):

        delta = event.globalPosition().toPoint() - self.drag_position
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.drag_position = event.globalPosition().toPoint()

    def say(self, text):

        self.text.setText(text)

    