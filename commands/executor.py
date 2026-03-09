import os
import subprocess
import ctypes


class CommandExecutor:

    def execute(self, command, param):

        if command == "open_browser":

            print("Открываю браузер")

            # открывает браузер по умолчанию
            os.system("start https://www.google.com")

        elif command == "open_notepad":

            print("Открываю блокнот")

            subprocess.Popen("notepad.exe")

        elif command == "shutdown":

            print("Выключение компьютера")

            os.system("shutdown /s /t 5")

        elif command == "restart":

            print("Перезагрузка компьютера")

            os.system("shutdown /r /t 5")

        elif command == "type_text":

            print("Текст:", param)

        elif command == "lock_pc":

            print("Блокировка компьютера")

            ctypes.windll.user32.LockWorkStation()

        elif command == "exit":

            print("Завершение программы")

            return False

        else:

            print("Команда не распознана")

        return True