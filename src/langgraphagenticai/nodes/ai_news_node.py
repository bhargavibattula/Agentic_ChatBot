from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate
import os


class AINewsNode:
    def __init__(self,llm):
        """
        Initialize the AINewsNode with API keys for Tavily and GROQ.
        """
        self.tavily = TavilyClient()
        self.llm = llm
        # this is used to capture various steps in this file so that later can be use for steps shown
        self.state = {}

    def fetch_news(self, state: dict) -> dict:
        """
        Fetch AI news based on the specified frequency.
        """
        # Ensure fresh Tavily Client with latest key
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
             return {"messages": [AIMessage(content="Error: Tavily API Key is missing. Please enter it in the sidebar.")]}
        self.tavily = TavilyClient(api_key=api_key)

        msgs = state.get('messages', [])
        if not msgs:
            return {}
            
        raw_content = msgs[0].content.lower().strip()
        
        time_range_map = {'daily': 'd', 'weekly': 'w', 'monthly': 'm', 'year': 'y'}
        days_map = {'daily': 1, 'weekly': 7, 'monthly': 30, 'year': 366}

        if 'weekly' in raw_content:
            frequency = 'weekly'
        elif 'monthly' in raw_content:
            frequency = 'monthly'
        elif 'year' in raw_content:
            frequency = 'year'
        else:
            frequency = 'daily'

        self.state['frequency'] = frequency
        
        try:
            response = self.tavily.search(
                query=f"Latest Artificial Intelligence (AI) technology news headlines: {raw_content}",
                topic="news",
                time_range=time_range_map[frequency],
                include_answer="advanced",
                max_results=10,
                days=days_map[frequency]
            )
            news_data = response.get('results', [])
            self.state['news_data'] = news_data
            return {"news_data": news_data}
        except Exception as e:
            return {"messages": [AIMessage(content=f"Error fetching news: {str(e)}")]}

    def summarize_news(self, state: dict) -> dict:
        """
        Summarize the news data found in the state.
        """
        news_items = state.get('news_data', [])

        if not news_items:
            return {"summary": "No relevant AI news articles were found for this query. Try a broader search term."}

        prompt_template = ChatPromptTemplate.from_messages([
            ("system", "Summarize these AI news articles into a professional markdown report with source links."),
            ("user", "Articles:\n{articles}")
        ])

        articles_str = "\n\n".join([
            f"Title: {item.get('title', '')}\nContent: {item.get('content', '')}\nURL: {item.get('url', '')}"
            for item in news_items
        ])

        try:
            response = self.llm.invoke(prompt_template.format(articles=articles_str))
            return {"summary": response.content}
        except Exception as e:
            return {"summary": f"Could not generate summary: {str(e)}"}
    
    def save_result(self, state: dict) -> dict:
        """
        Save outcome and append as AIMessage.
        """
        frequency = self.state.get('frequency', 'daily')
        summary = state.get('summary', 'No summary available.')

        dir_path = "./src/AINews"
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            
        filename = f"{dir_path}/{frequency}_summary.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        # Consistent return format for display_result to pick up
        from langchain_core.messages import AIMessage
        return {"messages": [AIMessage(content=summary)]}

