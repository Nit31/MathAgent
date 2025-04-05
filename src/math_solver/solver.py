import os
from typing import Dict

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from math_solver.graph import Agent


class Solver:
    """
    A class to solve mathematical problems using OpenAI's GPT-4o model.
    """
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

        self.agent = Agent(
            llm=self.llm,
        )

    def solve(self, problem: str) -> Dict[str, str]:
        """
        Solve a given mathematical problem using the agent.
        :param problem: The mathematical problem to solve.
        :return: The solution to the problem.
        """
        try:
            response = self.agent(problem)
        except Exception as e:
            print(f"Error occurred while solving the problem: {e}")
            return str(e)

        return response
