from sentence_transformers import SentenceTransformer, util
from logger import get_logger

logger = get_logger("NLP")


class NLPProcessor:

    def __init__(self):

        logger.info("Загрузка NLP модели (LaBSE)...")

        self.model = SentenceTransformer('sentence-transformers/LaBSE')

        logger.info("NLP модель успешно загружена")

        self.commands = {
            "open_browser": ["открой браузер", "запусти интернет"],
            "open_notepad": ["открой блокнот"],
            "shutdown": ["выключи компьютер"],
            "restart": ["перезагрузи компьютер"],
            "lock_pc": ["заблокируй компьютер"]
        }

        self.embeddings = {}

        logger.info("Предварительное вычисление эмбеддингов команд")

        for intent, phrases in self.commands.items():
            self.embeddings[intent] = self.model.encode(
                phrases,
                convert_to_tensor=True
            )

        logger.info("Эмбеддинги команд подготовлены")

    def process(self, text):

        logger.info(f"Анализ команды: {text}")

        text_emb = self.model.encode(text, convert_to_tensor=True)

        best_intent = None
        best_score = 0.5

        for intent, emb_list in self.embeddings.items():

            scores = util.pytorch_cos_sim(text_emb, emb_list)
            max_score = scores.max().item()

            logger.info(f"{intent} -> {max_score:.3f}")

            if max_score > best_score:
                best_score = max_score
                best_intent = intent

        logger.info(f"Определён интент: {best_intent}")

        return best_intent
