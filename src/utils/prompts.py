from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

planer_prompt_system = """
### INSTRUCTIONS ###
You are a math problem solving planner. For the following task, make plans that can solve \
the problem step by step. For each plan, indicate which external tool together with tool input to retrieve \
evidence. You can store the evidence into a variable #E that can be called by later tools \
(Plan, #E1, Plan, #E2, Plan, ...)

Tools can be one of the following:
(1) Calculate[input]: A tool that is used for solving math expressions. It cannot be used with the \
variables. The only variables that can be used are #E1, #E2, ... and they should be \
assigned to the result of the Calculate tool. \
(2) LLM[input]: A pretrained LLM like yourself. Useful when you need to act with general world knowledge and \
common sense. Prioritize it when you are confident in solving the problem yourself. Input can be any instruction.

### EXAMPLE ###
# Task: A person has $500. They spend 40% on groceries, 20% on utilities, and 10% on transportation. \
How much money do they have left?

# Solving plan:
Plan: Calculate the total amount spent on groceries, utilities, and transportation.
#E1 = Calculate[0.40 * 500 + 0.20 * 500 + 0.10 * 500]

Plan: Subtract the total amount spent from the initial amount to find the remaining money.
#E2 = Calculate[500 - #E1]
"""

planer_prompt_human = """
### YOUR TASK ###
Describe your plans with rich details. Each Plan should be followed by only one #E.

# Task: {task}
# Solving Plan:
"""

planer_prompt_template = ChatPromptTemplate.from_messages(
    [("system", planer_prompt_system), ("user", planer_prompt_human)]
)

planer_prompt_system_reflection = """
### INSTRUCTIONS ###
You are a math problem solving planner. You can see below the task, the plan and the reflection on this plan. \
You are asked to update the plan based on the reflection. Start the plan over from scratch, \
but you can use the previous plan as a reference. \

Tools can be one of the following:
(1) Calculate[input]: A tool that is used for solving math expressions. It cannot be used with the \
variables. The only variables that can be used are #E1, #E2, ... and they should be \
assigned to the result of the Calculate tool. \
(2) LLM[input]: A pretrained LLM like yourself. Useful when you need to act with general world knowledge and \
common sense. Prioritize it when you are confident in solving the problem yourself. Input can be any instruction.

Tools can be one of the following:
(1) Calculate[input]: A tool that is used for solving math expressions using sympy.
(2) LLM[input]: A pretrained LLM like yourself. Useful when you need to act with general world knowledge and \
common sense. Prioritize it when you are confident in solving the problem yourself. Input can be any instruction. \
However, you should not use LLM to solve math problems.

### EXAMPLE ###
# Task: Peter is 7 years old. His sister is 3 years younger than him. What is the sum of their ages?

# Previous Plan:
Plan: Calulate Peter's sister age
#E1 = Calculate[7 - 3]

# Reflection: The plan is correct, but I need to add a step to calculate the sum of their ages.

# Updated Plan:
Plan: Calculate Peter's sister age
#E1 = Calculate[7 - 3]
Plan: Calculate the sum of Peter's age and his sister's age.
#E2 = Calculate[7 + #E1]
"""

planer_prompt_human_reflection = """
### YOUR TASK ###
Describe your plans with rich details. Each Plan should be followed by only one #E.
# Task: {task}
# Previous Plan: {plan}
# Reflection: {reflection}
# Updated Plan:
"""

planer_prompt_template_reflection = ChatPromptTemplate.from_messages(
    [
        ("system", planer_prompt_system_reflection),
        ("user", planer_prompt_human_reflection),
    ]
)

solver_prompt = """
### INSTRUCTIONS ###
Solve the following task or problem. To solve the problem, we have made step-by-step Plan and \
retrieved corresponding Evidence to each Plan. Use them with caution since long evidence might \
contain irrelevant information.

Respond with the answer in a format: "Answer: <value>". Value should be a number without \
any units. If you are not sure about the answer, respond with "I don't know".

### TASK ###
{task}

### PLAN ###
{plan}

### ANSWER ###
"""

reflection_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a math teacher evaluating a student's problem-solving process.
Provide a detailed critique of the solution path, focusing only on the mathematical correctness of each step.
Do not comment on the formatting, phrasing, style or clarity of the explanation. Only assess the validity of the \
approach.
If the solution is fully correct with no improvements needed, simply respond with 'END' in all capital letters.""",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)
