import sys

from PySide6.QtWidgets import QApplication

from ui.assistant_widget import AssistantWidget
from assistant.speech_thread import SpeechThread
from assistant.assistant_controller import AssistantController
from assistant.wake_word_detector import WakeWordDetector
from nlp.nlp_processor import DynamicNLP
from commands.executor_dynamic import DynamicCommandExecutor


app = QApplication(sys.argv)

widget = AssistantWidget()
widget.show()

speech = SpeechThread()

wake = WakeWordDetector("заря")

nlp = DynamicNLP()

executor = DynamicCommandExecutor()

controller = AssistantController(
    widget,
    wake,
    speech,
    nlp,
    executor
)

speech.text_detected.connect(controller.process)

speech.start()

sys.exit(app.exec())