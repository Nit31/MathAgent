import re
from typing import Dict, List, TypedDict

from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, START, MessagesState, StateGraph

from utils.prompts import planer_prompt_template, planer_prompt_template_reflection, reflection_prompt, solver_prompt
from utils.tools import calculate, llm_tool


class AgentState(TypedDict):
    messages: List[MessagesState]
    task: str
    plan_string: str
    steps: List
    results: Dict
    result: str
    reflection: str


class Agent:
    """Agent that solves math problems using a step-by-step approach."""
    def __init__(self, llm: ChatOpenAI):
        self.llm = llm
        self.graph = self._build_graph()

    def __call__(self, problem: str) -> Dict[str, str]:
        """Run the agent on a given problem
        Args:
            problem (str): The math problem to solve.
        Returns:
            str: The solution to the problem.
        """

        messages = [HumanMessage(content=problem)]

        result = self.graph.invoke({"task": problem, "messages": messages}, {"recursion_limit": 100})

        return {"answer": result["result"], "solution": "\n".join(m.pretty_repr() for m in result["messages"])}

    def _planner(self, state: AgentState) -> AgentState:
        """Worker node that generates a plan for the agent."""
        regex_pattern = r"Plan:\s*(.+)\s*(#E\d+)\s*=\s*(\w+)\s*\[([^\]]+)\]"

        task = state["task"]

        if "reflection" in state and state["reflection"] is not None:
            # If we have a reflection, we need to update the plan
            prompt = planer_prompt_template_reflection.format_messages(
                task=task,
                plan=state["plan_string"],
                reflection=state["reflection"],
            )

        else:
            # If we don't have a reflection, we need to create a new plan
            prompt = planer_prompt_template.format_messages(task=task)

        response = self.llm.invoke(prompt)

        # Extract the plan string from the response
        matches = re.findall(regex_pattern, response.content)

        updated_state = {
            "messages": state["messages"] + [response],
            "task": task,
            "plan_string": response.content,
            "steps": matches,
            "results": {},
            "result": None,
            "reflection": None,
        }

        return updated_state
    def _get_current_task(self, state: AgentState) -> int:
        """Get the current task to execute."""
        if "results" not in state or state["results"] is None:
            return 1
        if len(state["results"]) == len(state["steps"]):
            return None
        else:
            return len(state["results"]) + 1

    def _executor(self, state: AgentState) -> AgentState:
        """Worker node that executes the tools of a given plan."""
        _step = self._get_current_task(state)
        try:
            _, step_name, tool_name, tool_input = state["steps"][_step - 1]
        except TypeError:
            # There was an error in the plan
            updated_state = {
                "messages": state["messages"] + [AIMessage(content="Error in the plan.")],
                "task": state["task"],
                "plan_string": state["plan_string"],
                "steps": state["steps"],
                "results": {},
                "result": None,
                "reflection": None,
            }
            return updated_state

        _results = (state["results"] or {}) if "results" in state else {}
        for k, v in _results.items():
            tool_input = tool_input.replace(k, v)
        if tool_name == "Calculate":
            result = calculate.invoke(tool_input)
        elif tool_name == "LLM":
            result = llm_tool.invoke(tool_input, self.llm)
        else:
            raise ValueError
        _results[step_name] = str(result)

        tool_message = ToolMessage(content=f"{tool_input}\nResult: {result}", artifact=result, tool_call_id=step_name)

        updated_state = {
            "messages": state["messages"] + [tool_message],
            "task": state["task"],
            "plan_string": state["plan_string"],
            "steps": state["steps"],
            "results": _results,
            "result": None,
            "reflection": None,
        }

        return updated_state

    def _solve(self, state: AgentState) -> AgentState:
        """Worker node that generates the final result."""
        plan = ""
        for _plan, step_name, tool_name, tool_input in state["steps"]:
            _results = (state["results"] or {}) if "results" in state else {}
            for k, v in _results.items():
                tool_input = tool_input.replace(k, v)
                step_name = step_name.replace(k, v)
            plan += f"Plan: {_plan}\n{step_name} = {tool_name}[{tool_input}]"
        prompt = solver_prompt.format(plan=plan, task=state["task"])
        result = self.llm.invoke(prompt)

        updated_state = {
            "messages": state["messages"] + [result],
            "task": state["task"],
            "plan_string": state["plan_string"],
            "steps": state["steps"],
            "results": state["results"],
            "result": result.content,
            "reflection": None,
        }

        return updated_state

    def _reflection_node(self, state: AgentState) -> AgentState:
        """Worker node that generates the critical reflection."""
        # Other messages we need to adjust
        cls_map = {"ai": HumanMessage, "human": AIMessage, "tool": AIMessage}
        # First message is the original user request. We hold it the same for all nodes
        translated = [state["messages"][0]] + [cls_map[msg.type](content=msg.content) for msg in state["messages"][1:]]
        res = self.llm.invoke(
            reflection_prompt.format_messages(messages=translated),
            stop=["\n\n###"],
        )

        updated_state = {
            "messages": state["messages"] + [res],
            "task": state["task"],
            "plan_string": state["plan_string"],
            "steps": state["steps"],
            "results": state["results"],
            "result": state["result"],
            "reflection": res.content,
        }

        return updated_state

    def _route(self, state: AgentState) -> str:
        """Route the agent to the next node."""
        _step = self._get_current_task(state)
        if _step is None:
            # We have executed all tasks
            return "solve"
        else:
            # We are still executing tasks, loop back to the "tool" node
            return "tool"

    def _should_continue(self, state: AgentState) -> str:
        """Check if the agent should continue or stop."""
        if len([msg for msg in state["messages"] if isinstance(msg, AIMessage)]) > 3:
            # print("Reached the limit of messages")
            return END

        if "END" in state["reflection"]:
            # If the last message is "END", we stop
            # print("Reflection node returned END")
            return END

        return "plan"

    def _build_graph(self) -> StateGraph:
        """Build the state graph for the agent."""
        graph = StateGraph(AgentState)

        graph.add_node("plan", self._planner)
        graph.add_node("tool", self._executor)
        graph.add_node("solve", self._solve)
        graph.add_node("reflect", self._reflection_node)

        graph.add_edge(START, "plan")
        graph.add_edge("plan", "tool")
        graph.add_conditional_edges("tool", self._route)
        graph.add_edge("solve", "reflect")
        graph.add_conditional_edges("reflect", self._should_continue)

        return graph.compile()
