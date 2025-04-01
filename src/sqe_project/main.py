from agents import Project_Manager_Agents
from tasks import Project_Manager_Tasks
from crewai import Crew, Process, LLM
import litellm
import streamlit as st
import markdown
from dotenv import load_dotenv
from io import StringIO
import os

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("⚠️ GEMINI_API_KEY not found. Please check your .env file.")
    st.stop()

st.title("🛠️ AI Project Management Assistant")

############################################################################################
# Taking Inputs
############################################################################################

project_Title = st.text_input("Project Title")
Project_Requirements = st.text_area("Project Requirements")

def create_prompt_for_questions(project_title, project_requirements):
    prompt = f"""
        You are an AI assistant specializing in project analysis. Your task is to review the given project title and its existing requirements, then suggest **only the most important missing** features in the form of questions that ask about their addition.

        ### **Instructions:**
        - Carefully analyze the **project title** and **existing requirements**.
        - Identify **10 to 15 critical missing features** that would improve the project.
        - **Each missing feature must be framed as a question**, explicitly asking if it should be added.
        - The questions must be **feature-focused**, practical, and essential for project success.
        - Do **not** provide explanations or extra text—only the questions.

        ### **Output Format:**
        - The response should **only** contain 3 to 5 **clear, feature-related questions**.
        - Ensure each question starts with phrases like:
          - "Do you want to add..."
          - "Would you like to include..."
          - "Should the system have..."
          - "Do you need support for..."
          - "Would it be helpful to add..."

        ### **Project Title:** {project_title}  
        ### **Given Requirements:**  
        {project_requirements}
    """
    return prompt

def get_litellm_response(prompt):
    response = litellm.completion(
        model="gemini/gemini-2.0-flash-exp",  
        api_key=api_key,
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

# Session State Handling
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "answers" not in st.session_state:
    st.session_state.answers = {}

if st.button("Take Interview"):
    if project_Title and Project_Requirements:
        question_prompt = create_prompt_for_questions(project_Title, Project_Requirements)
        questions_response = get_litellm_response(question_prompt)
        st.session_state.chat_history = [q.strip() for q in questions_response.split("\n") if q.strip()]
        st.session_state.current_question = 0

# Store questions and answers in a structured dictionary
if "qa_pairs" not in st.session_state:
    st.session_state.qa_pairs = {}

# Display Questions
if st.session_state.chat_history:
    index = st.session_state.current_question
    if index < len(st.session_state.chat_history):  
        question = st.session_state.chat_history[index]
        st.subheader(f"🤖 Question {index+1}: {question}")
        user_answer = st.text_input("✏️ Your Answer", key=f"answer_{index}")

        if st.button("Next"):
            if user_answer.strip():
                 # Store question and answer together
                st.session_state.qa_pairs[question] = user_answer
                st.session_state.current_question += 1
                st.rerun()
            else:
                st.warning("⚠️ Please enter an answer before proceeding.")

############################################################################################
# Creating Agents and Tasks
############################################################################################

agents = Project_Manager_Agents()
tasks = Project_Manager_Tasks()

# Importing Agents
Project_Analysis_Agent = agents.Project_Analysis_Agent()
Task_Breakdown_Agent = agents.Task_Breakdown_Agent()
Risk_Analysis_Agent = agents.Risk_Analysis_Agent()
Final_Report_Agent = agents.Final_Report_Agent()

# Assigning Tasks
Project_Analysis_Task = tasks.Project_Analysis_Task(
    agent=Project_Analysis_Agent,
    project_Title=project_Title,
    Project_Requirements=Project_Requirements,
    further_context=st.session_state.qa_pairs
)

Task_Breakdown_Task = tasks.Task_Breakdown_Task(
    agent=Task_Breakdown_Agent,
    context=[Project_Analysis_Task],
)

Risk_Analysis_Task = tasks.Risk_Analysis_Task(
    agent=Risk_Analysis_Agent,
    context=[Task_Breakdown_Task],
)

Final_Report_Task = tasks.Final_Report_Task(
    agent=Final_Report_Agent,
    context=[Project_Analysis_Task, Task_Breakdown_Task, Risk_Analysis_Task],
)

############################################################################################
# Creating Crew
############################################################################################

crew = Crew(
    agents=[Project_Analysis_Agent, Task_Breakdown_Agent, Risk_Analysis_Agent, Final_Report_Agent],
    tasks=[Project_Analysis_Task, Task_Breakdown_Task, Risk_Analysis_Task, Final_Report_Task],
    verbose=True,
)

def save_output_to_markdown(output, filename="agent_output.md"):
    """Saves the output in a structured Markdown file."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write(output.replace("**", ""))

if st.button("Submit"):
    with st.spinner("Processing... Please wait"):
        results = crew.kickoff()
        output_text = results.raw if hasattr(results, 'raw') else str(results)
        st.markdown(output_text)
        output_buffer = StringIO()
        output_buffer.write(output_text)
        st.download_button(
            label="Download Report",
            data=output_buffer.getvalue(),
            file_name="project_report.md",
            mime="text/markdown"
        )
