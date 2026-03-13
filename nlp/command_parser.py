class NLPProcessor:

    def __init__(self):

        self.wake_word = "заря"

        self.intents = {

            "open_browser": [
                "открой браузер",
                "запусти браузер"
            ],

            "open_notepad": [
                "открой блокнот",
                "запусти блокнот"
            ],

            "shutdown": [
                "выключи компьютер",
                "выключи систему"
            ],

            "restart": [
                "перезагрузи компьютер"
            ],

            "lock_pc": [
                "заблокируй компьютер"
            ]

        }

    def process(self, text):

        if text is None:
            return None

        text = text.lower()

        if not text.startswith(self.wake_word):
            return None

        command_text = text.replace(self.wake_word, "").strip()

        for intent, phrases in self.intents.items():

            for phrase in phrases:

                if phrase in command_text:
                    return (intent, None)

        return ("unknown", command_text)