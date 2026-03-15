from logger import get_logger

logger = get_logger("NLP")

class DynamicNLP:

    def __init__(self):
        logger.info("DynamicNLP готов")

    def process(self, text):
        # возвращаем текст как есть
        return text