import time
from logger import get_logger

logger = get_logger("Controller")


class AssistantController:

    def __init__(self, widget, wake_detector, speech_thread, nlp, executor):
        self.widget = widget
        self.wake_detector = wake_detector
        self.speech = speech_thread
        self.nlp = nlp
        self.executor = executor

        self.waiting_command = False
        self.wake_time = 0

    def process(self, text):
        text = text.strip().lower()
        logger.info(f"Получен текст: {text}")

        # -----------------------
        # Режим ожидания команды
        # -----------------------
        if self.waiting_command:

            if text == "" or text == self.wake_detector.wake_word:
                # пустой звук или повторное "заря" → продолжаем слушать
                return

            logger.info(f"Обработка команды после wake word: {text}")

            command_text = self.nlp.process(text)

            self.widget.set_state("thinking")
            self.executor.execute(command_text)
            self.widget.say("Готово")
            self.waiting_command = False
            self.widget.set_state("idle")
            return

        # -----------------------
        # Проверка wake word
        # -----------------------
        if self.wake_detector.detect(text):
            logger.info("Заря активирована")
            self.widget.set_state("listening")
            self.widget.say("Слушаю")
            self.waiting_command = True
            self.wake_time = time.time()

            # если сразу была команда после wake word
            words = text.split()
            if len(words) > 1:
                command_text = " ".join(words[1:])
                command_text = self.nlp.process(command_text)
                logger.info(f"Обработка команды сразу после wake word: {command_text}")
                self.widget.set_state("thinking")
                self.executor.execute(command_text)
                self.widget.say("Готово")
                self.waiting_command = False
                self.widget.set_state("idle")