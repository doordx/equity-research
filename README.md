# 📊 Equity Research AI Agent

An AI-powered equity research system that uses ReAct (Reasoning + Acting) agents to perform comprehensive financial analysis, news sentiment analysis, and market research.

## ✨ Features

- **ReAct Agent Framework**: Step-by-step reasoning with tool execution
- **Financial Data Analysis**: Real-time stock data, financial statements, and key metrics via Yahoo Finance
- **News Sentiment Analysis**: Automated sentiment scoring of market news using TextBlob
- **Web & News Search**: DuckDuckGo integration for comprehensive market research
- **Financial Ratio Computation**: Automated calculation of valuation, profitability, and growth metrics
- **Company Scoring**: Heuristic-based scoring system for investment quality assessment

## 🏗️ Architecture

### Agents
- **[`BaseAgent`](agents/base_agent.py)**: Abstract base class for all agents
- **[`ReActAgent`](agents/react_agent.py)**: Main reasoning agent that follows the ReAct pattern (Thought → Action → Observation)

### Tools
- **[`FinanceDataTool`](tools/finance_data.py)**: Fetches stock prices, company info, and financial statements
- **[`WebSearchTool`](tools/web_search.py)**: DuckDuckGo search for web and news queries
- **[`FinancialAnalysisTool`](tools/financial_analysis.py)**: Computes financial ratios and company scores
- **[`NewsSentimentTool`](tools/news_sentiment.py)**: Analyzes sentiment from news articles

### Tool Registry
**[`ToolRegistry`](agents/tool_registry.py)** manages all available tools:
- `finance_data`: Get company summary and financials
- `price_history`: Fetch historical price data
- `search`: General web search
- `news`: News-specific search
- `financial_ratios`: Compute financial metrics
- `score_company`: Generate investment quality score
- `news_sentiment`: Analyze news sentiment

## 📋 Requirements

```
groq>=0.5.0
python-dotenv>=1.0.0
requests>=2.31.0
yfinance
pandas
duckduckgo-search
beautifulsoup4
textblob
```

## 🚀 Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd equity-research
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**:
Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_groq_api_key_here
```

4. **Get a Groq API Key**:
- Sign up at [https://console.groq.com](https://console.groq.com)
- Generate an API key
- Add it to your `.env` file

## 💻 Usage

### Basic Example

```python
from agents.react_agent import ReActAgent

# Initialize the agent
agent = ReActAgent()

# Run a query
query = "Get latest news about NVDA, analyze sentiment and provide a market interpretation."
result = agent.run(query)

print(result)
```

### Running the Main Script

```bash
python main.py
```

### Example Queries

```python
# Market sentiment analysis
"Get latest news about NVDA, analyze sentiment and provide a market interpretation."

# Company financial analysis
"Analyze Apple's financial health, calculate key ratios, and provide an investment recommendation."

# Price trend analysis
"Get TSLA price history for the past year and identify key trends."

# Comprehensive research
"Research Microsoft: get financial data, recent news, sentiment analysis, and provide a detailed investment thesis."
```

## 🔧 Configuration

Edit [`config.py`](config.py) to customize:

```python
MODEL_NAME = "llama-3.3-70b-versatile"  # Groq model to use
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
```

## 🤖 How ReAct Agent Works

The ReAct agent follows a reasoning loop:

1. **Thought**: Agent reasons about what to do next
2. **Action**: Agent selects a tool to execute
3. **Action Input**: Agent provides JSON parameters for the tool
4. **Observation**: Tool output is returned to the agent
5. **Repeat**: Agent continues until it has enough information
6. **Final Answer**: Agent provides comprehensive analysis

### Example ReAct Flow

```
Thought: I need to get news about NVDA first
Action: news
Action Input: {"query": "NVDA stock news"}

Observation: [{"title": "NVIDIA Announces...", ...}]

Thought: Now I should analyze the sentiment of these articles
Action: news_sentiment
Action Input: {"news_items": [...]}

Observation: {"overall_sentiment": "positive", ...}

Thought: I have enough information to provide an interpretation
Final Answer: Based on recent news analysis...
```

## 📊 Available Financial Metrics

The [`FinancialAnalysisTool`](tools/financial_analysis.py) computes:

**Valuation Ratios**
- P/E Ratio
- PEG Ratio
- Price-to-Book
- Price-to-Sales
- EV/Revenue
- EV/EBITDA

**Profitability Metrics**
- Gross Margin
- Net Margin

**Growth Metrics**
- Year-over-Year Revenue Growth

**Balance Sheet Metrics**
- Debt-to-Equity Ratio

**Cash Flow Metrics**
- Free Cash Flow

## 🎯 Company Scoring System

The scoring system evaluates companies based on:
- ✅ P/E Ratio < 20 (Reasonable valuation)
- ✅ Revenue Growth > 10% YoY (Strong growth)
- ✅ Net Margin > 10% (Profitable)
- ✅ Debt-to-Equity < 1 (Conservative leverage)

**Score Categories**:
- **Strong**: 3+ criteria met
- **Mixed**: 2 criteria met
- **Weak**: <2 criteria met

## 📁 Project Structure

```
equity-research/
├── agents/
│   ├── base_agent.py          # Abstract base agent class
│   ├── react_agent.py         # ReAct reasoning agent
│   └── tool_registry.py       # Tool management and routing
├── tools/
│   ├── finance_data.py        # Yahoo Finance integration
│   ├── financial_analysis.py # Ratio computation and scoring
│   ├── news_sentiment.py     # Sentiment analysis
│   └── web_search.py         # DuckDuckGo search
├── config.py                 # Configuration settings
├── main.py                   # Entry point
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

## 🔍 Technical Details

- **LLM Provider**: Groq (using Llama 3.3 70B)
- **Temperature**: 0.2 (for consistent reasoning)
- **Max Iterations**: 5 (prevents infinite loops)
- **Data Source**: Yahoo Finance (via yfinance)
- **Search Engine**: DuckDuckGo (privacy-friendly)
- **Sentiment Analysis**: TextBlob (polarity-based)

## ⚠️ Limitations

- Financial data accuracy depends on Yahoo Finance
- Sentiment analysis is basic (rule-based polarity scoring)
- Agent limited to 5 reasoning iterations
- No real-time market data streaming
- Scoring system is heuristic-based, not ML-powered

## 📝 License

This project is provided as-is for educational and research purposes.

---

**Disclaimer**: This tool is for educational and research purposes only. It is not financial advice. Always conduct your own due diligence and consult with qualified financial advisors before making investment decisions.
