from speech.speech_recognition_module import SpeechToText
from nlp.command_parser import CommandParser
from commands.executor import CommandExecutor


stt = SpeechToText()
nlp = CommandParser()
executor = CommandExecutor()

running = True

print("Голосовая система запущена")

while running:

    text = stt.recognize()

    command = nlp.parse(text)

    if command:

        running = executor.execute(command[0], command[1])