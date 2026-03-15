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

        logger.info(f"Получен текст: {text}")

        # режим ожидания команды
        if self.waiting_command:

            if time.time() - self.wake_time > 3:

                logger.info("Таймаут ожидания команды")

                self.waiting_command = False
                self.widget.set_state("idle")

                return

            self.handle_command(text)
            return

        # проверяем слово активации
        if self.wake_detector.detect(text):

            logger.info("Заря активирована")

            self.widget.set_state("listening")
            self.widget.say("Слушаю")

            self.waiting_command = True
            self.wake_time = time.time()

            # если команда была в той же фразе
            words = text.split()

            if len(words) > 1:

                command = " ".join(words[1:])
                self.handle_command(command)

    def handle_command(self, text):

        logger.info(f"Обработка команды: {text}")

        self.widget.set_state("thinking")

        intent = self.nlp.process(text)

        if intent is None:

            self.widget.say("Не понимаю команду")
            self.widget.set_state("idle")

            return

        logger.info(f"Определён интент: {intent}")

        self.widget.set_state("talking")

        self.executor.execute(intent)

        self.widget.say("Готово")

        self.waiting_command = False

        self.widget.set_state("idle")