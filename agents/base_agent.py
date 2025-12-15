class BaseAgent:
    def __init__(self, name: str):
        self.name = name

    def run(self, prompt: str) -> str:
        raise NotImplementedError("Subclasses should implement this")
