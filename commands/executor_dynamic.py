import os
import subprocess
import logging
import ctypes
from rapidfuzz import fuzz

# pywin32 для работы с окнами
import win32gui
import win32con

logger = logging.getLogger("Executor")
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")


# ================================
# Коды клавиш WinAPI
# ================================
VK_VOLUME_UP = 0xAF
VK_VOLUME_DOWN = 0xAE
VK_VOLUME_MUTE = 0xAD


class DynamicCommandExecutor:

    def __init__(self):
        self.program_aliases = {
            "телеграм": os.path.expandvars(r"%LOCALAPPDATA%/Telegram Desktop/Telegram.exe"),
            "браузер": r"C:/Program Files/Google/Chrome\Application/chrome.exe",
            "ворд": r"C:/Program Files/Microsoft Office/root/Office16\WINWORD.EXE",
            "пауэрпоинт": r"C:/Program Files/Microsoft Office/root/Office16/POWERPNT.EXE",
            "блокнот": "notepad",
            "проводник": "explorer",
        }

    # -------------------------------
    # Поиск alias
    # -------------------------------
    def _match_alias(self, text):
        text = text.lower().strip()
        best_score = 0
        best_alias = None

        for alias in self.program_aliases.keys():
            score = fuzz.partial_ratio(alias, text)
            if score > best_score:
                best_score = score
                best_alias = alias

        if best_score >= 70:
            return best_alias
        return None

    # -------------------------------
    # Нажатие клавиши (WinAPI)
    # -------------------------------
    def _press_key(self, key):
        ctypes.windll.user32.keybd_event(key, 0, 0, 0)
        ctypes.windll.user32.keybd_event(key, 0, 2, 0)

    # -------------------------------
    # Громкость
    # -------------------------------
    def _change_volume(self, step: float):
        try:
            presses = int(abs(step) * 20)  # масштаб

            if step > 0:
                logger.info("EXECUTOR: увеличиваем громкость")
                for _ in range(presses):
                    self._press_key(VK_VOLUME_UP)

            elif step < 0:
                logger.info("EXECUTOR: уменьшаем громкость")
                for _ in range(presses):
                    self._press_key(VK_VOLUME_DOWN)

        except Exception as e:
            logger.error(f"EXECUTOR: ошибка громкости: {e}")

    def _mute_volume(self):
        self._press_key(VK_VOLUME_MUTE)
        logger.info("EXECUTOR: mute")

    # -------------------------------
    # Основной execute
    # -------------------------------
    def execute(self, text: str):
        if not text:
            return

        text = text.lower().strip()
        logger.info(f"EXECUTOR: получен текст: '{text}'")

        # -------------------------------
        # Системные команды
        # -------------------------------
        if self._handle_system_commands(text):
            return

        # -------------------------------
        # Громкость
        # -------------------------------
        if "громк" in text or "звук" in text:
            if "увелич" in text or "громче" in text:
                self._change_volume(0.05)

            elif "уменьш" in text or "тише" in text:
                self._change_volume(-0.05)

            elif "отключ" in text or "мьют" in text:
                self._mute_volume()

            return

        # -------------------------------
        # Управление окнами
        # -------------------------------
        if "закрой окно" in text:
            self._close_active_window()
            return

        if "сверни окно" in text:
            self._minimize_active_window()
            return

        # -------------------------------
        # Запуск программ
        # -------------------------------
        alias = self._match_alias(text)
        if alias:
            program_path = self.program_aliases[alias]
            logger.info(f"EXECUTOR: запуск '{alias}' -> '{program_path}'")

            if os.path.exists(program_path) or program_path in ["notepad", "explorer"]:
                try:
                    subprocess.Popen(f'start "" "{program_path}"', shell=True)
                except Exception as e:
                    logger.error(f"EXECUTOR: ошибка запуска: {e}")
            else:
                logger.error(f"EXECUTOR: файл не найден: {program_path}")
        else:
            logger.info("EXECUTOR: команда не распознана")

    # -------------------------------
    # Системные команды
    # -------------------------------
    def _handle_system_commands(self, text: str):
        if any(word in text for word in ["выключи", "shutdown"]):
            logger.info("EXECUTOR: shutdown")
            os.system("shutdown /s /t 1")
            return True

        if any(word in text for word in ["перезагруз", "restart"]):
            logger.info("EXECUTOR: restart")
            os.system("shutdown /r /t 1")
            return True

        if any(word in text for word in ["блок", "lock"]):
            logger.info("EXECUTOR: lock")
            os.system("rundll32.exe user32.dll,LockWorkStation")
            return True

        return False

    # -------------------------------
    # Закрыть окно
    # -------------------------------
    def _close_active_window(self):
        hwnd = win32gui.GetForegroundWindow()
        if hwnd:
            title = win32gui.GetWindowText(hwnd)
            win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
            logger.info(f"EXECUTOR: закрыто окно '{title}'")

    # -------------------------------
    # Свернуть окно
    # -------------------------------
    def _minimize_active_window(self):
        hwnd = win32gui.GetForegroundWindow()
        if hwnd:
            title = win32gui.GetWindowText(hwnd)
            win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
            logger.info(f"EXECUTOR: свернуто окно '{title}'")