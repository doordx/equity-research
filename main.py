from agents.react_agent import ReActAgent

def main():
    agent = ReActAgent()

    query = "Get latest news about NVDA, analyze sentiment and provide a market interpretation."
    result = agent.run(query)

    print("\n====== FINAL ANSWER ======")
    print(result)

if __name__ == "__main__":
    main()
