import json
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer


class SpeechService:

    _instance = None

    def __new__(cls):

        if cls._instance is None:

            print("Загрузка модели Vosk...")

            cls._instance = super().__new__(cls)

            cls._instance.model = Model("model/vosk-model-ru-0.42")
            cls._instance.q = queue.Queue()

        return cls._instance


    def callback(self, indata, frames, time, status):

        if status:
            print(status)

        self.q.put(bytes(indata))


    def listen(self):

        samplerate = 16000

        with sd.RawInputStream(
                samplerate=samplerate,
                blocksize=8000,
                dtype="int16",
                channels=1,
                callback=self.callback):

            rec = KaldiRecognizer(self.model, samplerate)

            print("Слушаю...")

            while True:

                data = self.q.get()

                if rec.AcceptWaveform(data):

                    result = json.loads(rec.Result())

                    text = result.get("text", "")

                    if text != "":
                        print("Распознано:", text)
                        return text