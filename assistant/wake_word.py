import pvporcupine
import pyaudio
from logger import get_logger

logger = get_logger("WakeWord")

class WakeWordEngine:

    def __init__(self):

        logger.info("Запуск wake-word engine")

        self.porcupine = pvporcupine.create(
            keywords=["computer"]
        )

        self.audio = pyaudio.PyAudio()

        self.stream = self.audio.open(
            rate=self.porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.porcupine.frame_length
        )

    def detect(self):

        pcm = self.stream.read(self.porcupine.frame_length)

        pcm = memoryview(pcm).cast('h')

        result = self.porcupine.process(pcm)

        if result >= 0:
            logger.info("Wake word detected")
            return True

        return False