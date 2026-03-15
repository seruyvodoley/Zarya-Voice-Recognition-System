import time
import pyttsx3
from logger import get_logger
from assistant.nlp_processor import NLPProcessor
from assistant.command_executor import CommandExecutor

logger = get_logger("Assistant")


class AssistantController:

    def __init__(self, widget, wake_detector, speech_thread):

        self.widget = widget
        self.wake = wake_detector
        self.speech = speech_thread

        self.state = "IDLE"
        self.command_timeout = 3
        self.command_start = None

        logger.info("Инициализация NLP")
        self.nlp = NLPProcessor()

        logger.info("Инициализация Executor")
        self.executor = CommandExecutor()

        self.tts = pyttsx3.init()

    def process(self, text):

        logger.info(f"Получен текст: {text}")

        text = text.lower().strip()

        # ---------- режим ожидания ----------
        if self.state == "IDLE":

            if self.wake.detect(text):

                logger.info("Wake word обнаружен")

                self.widget.set_state("listening")
                self.widget.say("Слушаю")

                self.tts.say("Слушаю")
                self.tts.runAndWait()

                self.state = "LISTENING"
                self.command_start = time.time()

        # ---------- режим команды ----------
        elif self.state == "LISTENING":

            # проверка таймаута
            if time.time() - self.command_start > self.command_timeout:

                logger.info("Таймаут ожидания команды")

                self.widget.set_state("idle")
                self.widget.say("")

                self.state = "IDLE"
                return

            intent = self.nlp.process(text)

            if intent:

                logger.info(f"Команда распознана: {intent}")

                self.widget.set_state("thinking")
                self.widget.say("Выполняю")

                self.executor.execute(intent)

                self.widget.set_state("idle")

                self.tts.say("Выполняю")
                self.tts.runAndWait()

                self.state = "IDLE"

            else:

                logger.info("Команда не распознана")

                self.widget.say("Не поняла команду")