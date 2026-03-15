import os
import webbrowser


class CommandExecutor:

    def execute(self, intent):

        if intent == "open_browser":

            webbrowser.open("https://google.com")

        elif intent == "open_notepad":

            os.system("notepad")

        elif intent == "shutdown":

            os.system("shutdown /s /t 1")

        elif intent == "restart":

            os.system("shutdown /r /t 1")

        elif intent == "lock_pc":

            os.system("rundll32.exe user32.dll,LockWorkStation")