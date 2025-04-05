import os

from dotenv import load_dotenv
from langchain.schema import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from utils.prompts import problem_prompt, system_prompt


class Solver:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()

        # Get API key from environment or prompt user
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("OpenAI API key not found in environment variables")

        self.llm = ChatOpenAI(
            openai_api_key=openai_api_key,
            model_name="gpt-4o-mini-2024-07-18",
            temperature=0,
            seed=42,
        )
        self.system_message = SystemMessage(content=system_prompt)

    def solve(self, problem: str) -> str:
        human_message = HumanMessage(content=problem_prompt.format(problem=problem))
        response = self.llm.invoke([self.system_message, human_message])
        return response.content
