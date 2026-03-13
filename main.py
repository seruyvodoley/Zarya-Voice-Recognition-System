from services.speech_service import SpeechService
from nlp.command_parser import NLPProcessor
from commands.executor import CommandExecutor
from commands.router import CommandRouter


speech = SpeechService()

nlp = NLPProcessor()

executor = CommandExecutor()
router = CommandRouter(executor)

print("Ассистент Заря запущен")

while True:

    text = speech.listen()

    result = nlp.process(text)

    if result:

        intent, param = result

        router.route(intent, param)