import time
import pyttsx3
from assistant.wake_word import WakeWordDetector
from assistant.speech_thread import SpeechThread
from assistant.nlp_processor import NLPProcessor
from assistant.command_executor import CommandExecutor

class AssistantController:
    def __init__(self, widget, wake_detector: WakeWordDetector, speech_thread: SpeechThread):
        self.widget = widget
        self.wake = wake_detector
        self.speech = speech_thread
        self.waiting_for_command = False
        self.command_start_time = None
        self.command_timeout = 3
        self.nlp = NLPProcessor()
        self.executor = CommandExecutor()
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 150)

    def process(self, text):
        if not text:
            return

        text = text.lower().strip()

        if self.waiting_for_command:
            if time.time() - self.command_start_time > self.command_timeout:
                self.widget.say("Команда не получена")
                self.widget.set_state("idle")
                self.waiting_for_command = False
                return

            intent = self.nlp.process(text)
            if intent:
                self.widget.set_state("thinking")
                self.widget.say(f"Выполняю: {intent}")
                self.executor.execute(intent)
                self.tts_engine.say(f"Выполняю: {intent}")
                self.tts_engine.runAndWait()
            else:
                self.widget.say("Команда не распознана")
                self.tts_engine.say("Команда не распознана")
                self.tts_engine.runAndWait()

            self.widget.set_state("idle")
            self.waiting_for_command = False

        elif self.wake.detect(text):
            self.widget.set_state("listening")
            self.widget.say("Слушаю...")
            self.waiting_for_command = True
            self.command_start_time = time.time()