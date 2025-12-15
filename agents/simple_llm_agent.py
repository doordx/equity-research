from groq import Groq
from config import GROQ_API_KEY, MODEL_NAME
from agents.base_agent import BaseAgent

class SimpleLLMAgent(BaseAgent):
    def __init__(self):
        super().__init__("SimpleLLMAgent")
        self.client = Groq(api_key=GROQ_API_KEY)

    def run(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        return response.choices[0].message.content
