from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from logger import get_logger

logger = get_logger("NLP")


class NLPProcessor:

    def __init__(self):

        logger.info("Инициализация NLP")

        self.commands = {
            "open_browser": [
                "открой браузер",
                "запусти браузер",
                "открой интернет"
            ],

            "open_notepad": [
                "открой блокнот",
                "запусти блокнот"
            ],

            "shutdown": [
                "выключи компьютер"
            ],

            "restart": [
                "перезагрузи компьютер"
            ],

            "lock_pc": [
                "заблокируй компьютер"
            ]
        }

        phrases = []
        self.intent_map = []

        for intent, examples in self.commands.items():

            for text in examples:

                phrases.append(text)
                self.intent_map.append(intent)

        self.vectorizer = TfidfVectorizer()

        self.matrix = self.vectorizer.fit_transform(phrases)

        logger.info("NLP готов")

    def process(self, text):

        vec = self.vectorizer.transform([text])

        scores = cosine_similarity(vec, self.matrix)

        best_index = scores.argmax()
        best_score = scores[0][best_index]

        logger.info(f"NLP score: {best_score}")

        if best_score < 0.35:
            return None

        return self.intent_map[best_index]