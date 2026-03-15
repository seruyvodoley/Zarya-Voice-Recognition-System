from rapidfuzz import fuzz

class WakeWordDetector:

    def __init__(self, wake_word="заря", threshold=90):
        self.wake_word = wake_word.lower()
        self.threshold = threshold

    def detect(self, text):
        if not text:
            return False

        words = text.lower().split()

        for word in words:
            score = fuzz.ratio(word, self.wake_word)
            if score >= self.threshold:
                return True

        return False