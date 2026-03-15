import os
import subprocess
from rapidfuzz import fuzz
import logging

logger = logging.getLogger("Executor")
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

class DynamicCommandExecutor:
    def __init__(self):
        # alias -> полный путь программы
        self.program_aliases = {
            "телеграм": os.path.expandvars(r"%LOCALAPPDATA%\Telegram Desktop\Telegram.exe"),
            "telegram": os.path.expandvars(r"%LOCALAPPDATA%\Telegram Desktop\Telegram.exe"),
            "браузер": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            "ворд": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
            "word": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
            "пауэрпоинт": r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE",
            "powerpoint": r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE",
            "блокнот": "notepad",
            "проводник": "explorer",
        }

    def _match_alias(self, text):
        text = text.lower().strip()
        best_score = 0
        best_alias = None
        for alias in self.program_aliases.keys():
            score = fuzz.partial_ratio(alias.lower(), text)
            if score > best_score:
                best_score = score
                best_alias = alias
        if best_score >= 70:
            return best_alias
        return None

    def execute(self, text: str):
        if not text:
            return
        logger.info(f"EXECUTOR: получен текст для выполнения: '{text}'")

        # системные команды
        if self._handle_system_commands(text):
            return

        # поиск alias
        alias = self._match_alias(text)
        if alias:
            program_path = self.program_aliases[alias]
            logger.info(f"EXECUTOR: запуск '{alias}' -> '{program_path}'")
            if os.path.exists(program_path) or program_path in ["notepad", "explorer"]:
                try:
                    subprocess.Popen(f'start "" "{program_path}"', shell=True)
                except Exception as e:
                    logger.error(f"EXECUTOR: ошибка при запуске {program_path}: {e}")
            else:
                logger.error(f"EXECUTOR: файл {program_path} не найден")
        else:
            logger.info("EXECUTOR: команда не распознана")

    def _handle_system_commands(self, text: str):
        text = text.lower()
        if any(word in text for word in ["выключи", "выключение", "shutdown"]):
            logger.info("EXECUTOR: выполняем shutdown")
            os.system("shutdown /s /t 1")
            return True
        if any(word in text for word in ["перезагруз", "restart"]):
            logger.info("EXECUTOR: выполняем restart")
            os.system("shutdown /r /t 1")
            return True
        if any(word in text for word in ["блок", "lock"]):
            logger.info("EXECUTOR: выполняем lock")
            os.system("rundll32.exe user32.dll,LockWorkStation")
            return True
        return False