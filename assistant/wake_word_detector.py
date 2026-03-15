class WakeWordDetector:

    def __init__(self, wake_word="заря"):

        self.wake_word = wake_word.lower()

    def detect(self, text):

        if not text:
            return False

        words = text.lower().split()

        return self.wake_word in words