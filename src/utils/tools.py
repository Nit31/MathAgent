import sympy as sp
from langchain_core.messages import SystemMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI


# Define a sympy-based tool
@tool
def calculate(expression: str) -> str:
    """Calculate an arithmetic expression using sympy.

    Args:
        expression: arithmetic expression as a string (e.g., '3 + 4')

    Returns:
        The evaluated result as a string.
    """
    try:
        expr = sp.sympify(expression)
        evaluated = expr.evalf() if expr.is_number else expr
        return str(evaluated)
    except Exception as e:
        return f"Error: {e}"


# Define a LLM tool
@tool
def llm_tool(expression: str, llm: ChatOpenAI) -> str:
    """Use LLM like yourself to process the input string.
    This is useful for tasks that require reasoning or understanding of the context.
    For example, you can use it to provide explanations.

    Args:
        expression: input string to be processed by LLM

    Returns:
        The processed output as a string.
    """
    response = llm.invoke([SystemMessage(content=expression)])
    return response.content


# Augment the LLM with the sympy tool
tools = [calculate, llm_tool]
tools_by_name = {tool.name: tool for tool in tools}
