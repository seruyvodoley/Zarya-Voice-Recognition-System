import sys
from PySide6.QtWidgets import QApplication
from ui.assistant_widget import AssistantWidget
from assistant.speech_thread import SpeechThread
from assistant.assistant_controller import AssistantController
from assistant.wake_word_detector import WakeWordDetector

app = QApplication(sys.argv)

widget = AssistantWidget()
widget.show()

wake = WakeWordDetector("заря")
speech = SpeechThread()

controller = AssistantController(widget, wake, speech)
speech.text_detected.connect(controller.process)
speech.start()

sys.exit(app.exec())