class WakeWordDetector:

    def __init__(self):

        self.wake_word = "заря"

    def detect(self, text):

        if text is None:
            return False

        text = text.lower()

        return self.wake_word in text