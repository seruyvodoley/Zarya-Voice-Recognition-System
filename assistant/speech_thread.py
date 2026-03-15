import queue
import json
import sounddevice as sd
from vosk import Model, KaldiRecognizer
from PySide6.QtCore import QThread, Signal
from logger import get_logger

logger = get_logger("Speech")


class SpeechThread(QThread):

    text_detected = Signal(str)

    def __init__(self):

        super().__init__()

        logger.info("Загрузка модели VOSK")

        self.model = Model("model/vosk-model-small-ru-0.22")

        self.rec = KaldiRecognizer(self.model, 16000)

        self.q = queue.Queue()

    def callback(self, indata, frames, time, status):

        self.q.put(bytes(indata))

    def run(self):

        logger.info("Микрофон активирован")

        with sd.RawInputStream(
                samplerate=16000,
                blocksize=8000,
                dtype='int16',
                channels=1,
                callback=self.callback):

            while True:

                data = self.q.get()

                if self.rec.AcceptWaveform(data):

                    result = json.loads(self.rec.Result())

                    text = result.get("text", "")

                    if text:
                        logger.info(f"Распознано: {text}")

                        self.text_detected.emit(text)