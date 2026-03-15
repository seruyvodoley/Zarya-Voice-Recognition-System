from rapidfuzz import fuzz


class WakeWordDetector:

    def __init__(self, wake_word="заря"):

        self.wake_word = wake_word

    def detect(self, text):

        if not text:
            return False

        words = text.lower().split()

        for word in words:

            score = fuzz.ratio(word, self.wake_word)

            if score > 80:
                return True

        return False