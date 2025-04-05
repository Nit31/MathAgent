import time

import requests
import streamlit as st

st.set_page_config(page_title="Math Problem Solver", layout="wide")

# Initialize session state for storing history
if "history" not in st.session_state:
    st.session_state.history = []


# API interaction functions
def submit_problem(problem):
    base_url = "http://localhost:8080"
    response = requests.post(f"{base_url}/submit-problem/", json={"problem": problem})
    if response.status_code == 200:
        return response.json()["problem_hash"]
    else:
        st.error(f"Failed to submit problem: {response.text}")
        return None


def get_solution(problem_hash):
    base_url = "http://localhost:8080"
    response = requests.get(f"{base_url}/get-solution/{problem_hash}")
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to retrieve solution: {response.text}")
        return None


# UI Components
st.title("Math Problem Solver")
st.write("Submit a math problem and get a step-by-step solution!")

# Example problems
examples = {
    "1": "Toulouse has twice as many sheep as Charleston. Charleston has 4 times as many sheep as Seattle. How many \
sheep do Toulouse, Charleston, and Seattle have together if Seattle has 20 sheep?",
    "2": "In a dance class of 20 students, 20% enrolled in contemporary dance, 25% of the remaining enrolled in jazz \
dance, and the rest enrolled in hip-hop dance. What percentage of the entire students enrolled in hip-hop dance?",
    "3": "I have 10 liters of orange drink that are two-thirds water and I wish to add it to 15 liters of pineapple \
drink that is three-fifths water. But as I pour it, I spill one liter of the orange drink. How much water is in the remaining 24 liters?",
}

# Sidebar with examples
st.sidebar.header("Example Problems")
selected_example = st.sidebar.selectbox("Choose an example", list(examples.keys()))
if st.sidebar.button("Use Example"):
    st.session_state.problem = examples[selected_example]

# Problem input
problem = st.text_area("Enter your math problem:", value=st.session_state.get("problem", ""), height=100)

col1, col2 = st.columns([1, 5])
submit = col1.button("Submit Problem")

# Process submission
if submit and problem:
    with st.spinner("Submitting problem..."):
        problem_hash = submit_problem(problem)

    if problem_hash:
        st.info("Problem submitted successfully!")

        # Try to get the solution with a delay to allow processing
        with st.spinner("Getting solution..."):
            # Try up to 3 times with a delay
            solution_data = None
            for _ in range(30):
                solution_data = get_solution(problem_hash)
                if solution_data and "solution" in solution_data:
                    break
                time.sleep(1)

        if solution_data and "solution" in solution_data:
            # Add to history
            st.session_state.history.append(
                {
                    "problem": problem,
                    "solution": solution_data["solution"],
                    "answer": solution_data["answer"],
                    "hash": problem_hash,
                }
            )

            # Show the recent solution
            st.subheader("Solution")
            st.write(solution_data["solution"])

            st.subheader("Answer")
            st.write(solution_data["answer"])
        else:
            st.warning("Solution is still being generated or not available yet. You can check history later.")

            # Still add to history for later checking
            st.session_state.history.append({"problem": problem, "hash": problem_hash, "pending": True})

# Display history
if st.session_state.history:
    st.header("Problem History")

    for i, item in enumerate(reversed(st.session_state.history)):
        with st.expander(f"Problem {i + 1}: {item['problem'][:50]}..."):
            st.write("**Problem:**")
            st.write(item["problem"])

            if item.get("pending"):
                if st.button(f"Check solution status for Problem {i + 1}"):
                    solution_data = get_solution(item["hash"])
                    if solution_data and "solution" in solution_data:
                        # Update history
                        item["solution"] = solution_data["solution"]
                        item["answer"] = solution_data["answer"]
                        item.pop("pending", None)
                        st.rerun()
                    else:
                        st.warning("Solution is still being processed.")
            else:
                st.write("**Solution:**")
                st.write(item["solution"])
                st.write("**Answer:**")
                st.write(item["answer"])
