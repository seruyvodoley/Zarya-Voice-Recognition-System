class CommandParser:

    def parse(self, text):

        if text is None:
            return None

        if "браузер" in text:
            return ("open_browser", None)

        if "блокнот" in text:
            return ("open_notepad", None)

        if "закрой окно" in text:
            return ("close_window", None)

        if "выключи компьютер" in text:
            return ("shutdown", None)

        return ("unknown", text)