from textblob import TextBlob

class NewsSentimentTool:
    """
    Performs sentiment analysis on news articles and returns structured insights.
    """

    def analyze(self, news_items: list):
        """
        news_items: list of dicts from DuckDuckGo search
            [{ "title": "...", "snippet": "...", "url": "..."}, ...]

        Returns:
            sentiment, average polarity, article-level sentiment breakdown
        """
        results = []
        total_score = 0
        count = 0

        for article in news_items:
            text = f"{article.get('title', '')}. {article.get('snippet', '')}"
            polarity = TextBlob(text).sentiment.polarity

            score = "positive" if polarity > 0.15 else \
                    "negative" if polarity < -0.15 else "neutral"

            results.append({
                "title": article.get("title"),
                "snippet": article.get("snippet"),
                "polarity": polarity,
                "sentiment": score
            })

            total_score += polarity
            count += 1

        avg_polarity = total_score / count if count > 0 else 0

        overall = (
            "positive" if avg_polarity > 0.1 else
            "negative" if avg_polarity < -0.1 else
            "neutral"
        )

        return {
            "overall_sentiment": overall,
            "average_polarity": avg_polarity,
            "articles": results
        }
