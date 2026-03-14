class WakeWordDetector:
    def __init__(self, wake_word="заря"):
        self.wake_word = wake_word.lower()

    def detect(self, text):
        if text:
            return self.wake_word in text.lower()
        return False