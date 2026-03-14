import queue
import json
import sounddevice as sd
from PySide6.QtCore import QThread, Signal
from vosk import Model, KaldiRecognizer
from logger import get_logger

logger = get_logger("SpeechThread")


class SpeechThread(QThread):

    text_detected = Signal(str)

    def __init__(self, model_path="model/vosk-model-small-ru-0.22"):
        super().__init__()

        logger.info("Загрузка модели VOSK...")

        self.model = Model(model_path)
        self.rec = KaldiRecognizer(self.model, 16000)

        logger.info("Модель VOSK успешно загружена")

        self.q = queue.Queue()

    def callback(self, indata, frames, time, status):
        self.q.put(bytes(indata))

    def run(self):

        logger.info("Запуск потока распознавания речи")

        samplerate = 16000

        with sd.RawInputStream(
            samplerate=samplerate,
            blocksize=4000,
            dtype="int16",
            channels=1,
            callback=self.callback
        ):

            logger.info("Микрофон активирован")

            while True:

                data = self.q.get()

                if self.rec.AcceptWaveform(data):

                    result = json.loads(self.rec.Result())
                    text = result.get("text", "")

                    if text:
                        logger.info(f"Распознано: {text}")
                        self.text_detected.emit(text)
