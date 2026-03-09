import speech_recognition as sr

class AudioInput:

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def listen(self):

        with self.microphone as source:
            print("Слушаю команду...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        return audio