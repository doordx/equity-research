import json
import re
from groq import Groq
from agents.base_agent import BaseAgent
from agents.tool_registry import ToolRegistry
from config import GROQ_API_KEY, MODEL_NAME

SYSTEM_PROMPT = """
You are a ReAct agent that can reason step-by-step and use tools.

Available Tools:
1. finance_data: {"ticker": "AAPL"}
2. price_history: {"ticker": "AAPL"}
3. search: {"query": "company news"}
4. news: {"query": "company news"}
5. financial_ratios: {"summary": {...}, "financials": {...}}
6. score_company: {"ratios": {...}}
7. news_sentiment: {"news_items": [...]}

Follow this REQUIRED format:

Thought: your reasoning
Action: tool_name
Action Input: JSON parameters

After tool output is shown to you as:
Observation: {...}

You MUST continue the reasoning loop until done.

End with:
Final Answer: your summary
"""

class ReActAgent(BaseAgent):
    def __init__(self):
        super().__init__("ReActAgent")
        self.client = Groq(api_key=GROQ_API_KEY)
        self.registry = ToolRegistry()

    def run(self, user_query: str):
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_query}
        ]

        output = ""
        for _ in range(5):  # limit # of iterations
            response = self.client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                temperature=0.2
            )
            output = response.choices[0].message.content
            print("\n--- LLM Step ---")
            print(output)

            # Check if final answer
            if "Final Answer:" in output:
                return output.split("Final Answer:")[-1].strip()

            # Parse Action + Action Input
            tool_name = self._extract_action(output)
            tool_input = self._extract_action_input(output)

            # Run tool
            observation = self.registry.call(tool_name, **tool_input)

            # Add tool result to conversation
            messages.append({"role": "assistant", "content": output})
            messages.append({"role": "user", "content": f"Observation: {observation}"})

        return "Reached max iteration limit."

    def _extract_action(self, text: str):
        for line in text.splitlines():
            if line.startswith("Action:"):
                return line.replace("Action:", "").strip()
        raise ValueError("No Action found.")

    def _extract_action_input(self, text: str):
        for line in text.splitlines():
            if line.startswith("Action Input:"):
                json_str = line.replace("Action Input:", "").strip()
                
                # Try to extract JSON from code blocks if present
                if json_str.startswith("```"):
                    json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', json_str, re.DOTALL)
                    if json_match:
                        json_str = json_match.group(1)
                
                # Replace {...} placeholders with {} to make valid JSON
                json_str = re.sub(r'\{\s*\.\.\.\s*\}', '{}', json_str)
                
                # Handle common JSON issues
                try:
                    # First, try parsing as-is
                    return json.loads(json_str)
                except json.JSONDecodeError as e:
                    # Try fixing single quotes to double quotes
                    try:
                        # Replace single quotes with double quotes (careful approach)
                        fixed_str = json_str.replace("'", '"')
                        return json.loads(fixed_str)
                    except json.JSONDecodeError:
                        # If still fails, print helpful error message
                        print(f"\n=== JSON Parse Error ===")
                        print(f"Original error: {e}")
                        print(f"Attempted to parse: {json_str}")
                        print(f"======================\n")
                        raise ValueError(f"Failed to parse Action Input as JSON: {json_str[:100]}...")
        raise ValueError("No Action Input found.")
