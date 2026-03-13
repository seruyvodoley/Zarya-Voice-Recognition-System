import os
import subprocess
import ctypes


class CommandExecutor:

    def open_browser(self, param):

        print("Открываю браузер")

        os.system("start https://www.google.com")

    def open_notepad(self, param):

        print("Открываю блокнот")

        subprocess.Popen("notepad.exe")

    def shutdown(self, param):

        print("Выключение компьютера")

        os.system("shutdown /s /t 5")

    def restart(self, param):

        print("Перезагрузка")

        os.system("shutdown /r /t 5")

    def lock_pc(self, param):

        print("Блокировка ПК")

        ctypes.windll.user32.LockWorkStation()