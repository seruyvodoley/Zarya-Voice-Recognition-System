import json
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer


class SpeechToText:

    def __init__(self):

        print("Загрузка модели распознавания...")

        self.model = Model("vosk-model-ru-0.42/vosk-model-ru-0.42")

        self.q = queue.Queue()

    def callback(self, indata, frames, time, status):

        if status:
            print(status)

        self.q.put(bytes(indata))

    def recognize(self):

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