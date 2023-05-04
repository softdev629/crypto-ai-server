from langchain.chat_models import ChatOpenAI
from langchain.tools import BaseTool
from langchain.utilities import GoogleSearchAPIWrapper, SerpAPIWrapper
from langchain.agents import load_tools
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(temperature=0, model_name="gpt-4")


class LatestInfoTool(BaseTool):
    name = "LatestInfo"
    description = "useful for providing latest information on crypto movements, news and prices"

    def _run(self, query: str) -> str:
        """Use the tool."""

        search = GoogleSearchAPIWrapper()

        return search.results(query, 5)

    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("LatestInfoTool does not support async")
