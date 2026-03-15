from sentence_transformers import SentenceTransformer, util
from logger import get_logger

logger = get_logger("NLP")


class NLPProcessor:

    def __init__(self):

        logger.info("Загрузка NLP модели...")

        self.model = SentenceTransformer(
            "paraphrase-multilingual-MiniLM-L12-v2"
        )

        logger.info("NLP модель загружена")

        self.commands = {
            "open_browser": [
                "открой браузер",
                "запусти интернет",
                "открой chrome"
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

        self.embeddings = {}

        for intent, phrases in self.commands.items():

            self.embeddings[intent] = self.model.encode(
                phrases,
                convert_to_tensor=True
            )

    def process(self, text):

        text_emb = self.model.encode(text, convert_to_tensor=True)

        best_intent = None
        best_score = 0.55

        for intent, emb_list in self.embeddings.items():

            scores = util.pytorch_cos_sim(text_emb, emb_list)
            score = scores.max().item()

            logger.info(f"{intent} -> {score}")

            if score > best_score:
                best_score = score
                best_intent = intent

        return best_intent