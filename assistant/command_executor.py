import subprocess
import os

class CommandExecutor:
    def execute(self, intent):
        if intent == "open_browser":
            subprocess.Popen(["start", "chrome"], shell=True)
        elif intent == "open_notepad":
            subprocess.Popen(["notepad.exe"])
        elif intent == "shutdown":
            os.system("shutdown /s /t 0")
        elif intent == "restart":
            os.system("shutdown /r /t 0")
        elif intent == "lock_pc":
            os.system("rundll32.exe user32.dll,LockWorkStation")