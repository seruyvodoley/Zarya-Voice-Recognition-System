class CommandRouter:

    def __init__(self, executor):

        self.executor = executor

        self.routes = {
            "open_browser": executor.open_browser,
            "open_notepad": executor.open_notepad,
            "shutdown": executor.shutdown,
            "restart": executor.restart,
            "lock_pc": executor.lock_pc
        }

    def route(self, intent, param):

        if intent in self.routes:
            self.routes[intent](param)
            return True

        if intent == "unknown":
            print("Команда не распознана")

        return True