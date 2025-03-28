from agents import Project_Manager_Agents
from tasks import Project_Manager_Tasks
from crewai import Crew, Process, LLM
import streamlit as st
import markdown
from dotenv import load_dotenv
from io import StringIO
import os
import re

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Taking Inputs
project_Title = st.text_input("Project Title")
Project_Requirements = st.text_area("Project Requirements")

# Creating Objects of Agents and Tasks
agents = Project_Manager_Agents()
tasks = Project_Manager_Tasks()

# Importing all Agents
Missing_Requirements_Agent = agents.Missing_Requirements_Agent()  # Agent 1
Project_Analysis_Agent = agents.Project_Analysis_Agent()  # Agent 2
Task_Breakdown_Agent = agents.Task_Breakdown_Agent()  # Agent 3
Risk_Analysis_Agent = agents.Risk_Analysis_Agent()  # Agent 4
Final_Report_Agent = agents.Final_Report_Agent()  # Agent 5

# Assigning Tasks to Each Agent
# Task 1
Missing_Requirements_Task = tasks.Missing_Requirements_Task(
    agent=Missing_Requirements_Agent,
    project_Title=project_Title,
    Project_Requirements=Project_Requirements
)

# Process Missing Requirements
if st.button("Analyze Missing Requirements"):
    with st.spinner("Analyzing requirements..."):
        # missing_results = Missing_Requirements_Task.run()
        missing_results = tasks.Missing_Requirements_Task(
                agent=Missing_Requirements_Agent,
                project_Title=project_Title,
                Project_Requirements=Project_Requirements
            )
        enhanced_requirements = missing_results.output  # Extracting the enhanced requirements
        st.session_state["enhanced_requirements"] = enhanced_requirements  # Store in session state
        st.markdown("### Enhanced Requirements:")
        st.text_area("Updated Requirements", enhanced_requirements, height=200)

# Chatbot for User Interaction
if "enhanced_requirements" in st.session_state:
    st.markdown("### Chat with AI to refine requirements")
    user_input = st.text_input("Ask about project requirements:")
    if user_input:
        response = Missing_Requirements_Agent.chat(user_input)  # Simulate chat response
        st.markdown(f"**AI:** {response}")

# Assigning Next Tasks
# Task 2
Project_Analysis_Task = tasks.Project_Analysis_Task(
    agent=Project_Analysis_Agent,
    project_Title=project_Title,
    Project_Requirements=st.session_state.get("enhanced_requirements", Project_Requirements),
    context=[Missing_Requirements_Task]
)


# Task 3
Task_Breakdown_Task = tasks.Task_Breakdown_Task(
    agent = Task_Breakdown_Agent,
    context = [Project_Analysis_Task],

)

# Task 4
Risk_Analysis_Task = tasks.Risk_Analysis_Task(
    agent = Risk_Analysis_Agent,
    context = [Task_Breakdown_Task],

)

# Task 5
Final_Report_Task = tasks.Final_Report_Task(
    agent = Final_Report_Agent,
    context = [Project_Analysis_Task,Task_Breakdown_Task,Risk_Analysis_Task],

)

# Final Button to Execute All Tasks
if st.button("Submit for Full Analysis"):
    with st.spinner("Processing... Please wait"):
        crew = Crew(
            agents=[Missing_Requirements_Agent, Project_Analysis_Agent, Task_Breakdown_Agent, Risk_Analysis_Agent, Final_Report_Agent],
            tasks=[Missing_Requirements_Task, Project_Analysis_Task, Task_Breakdown_Task, Risk_Analysis_Task, Final_Report_Task],
            verbose=True,
        )
        results = crew.kickoff()
        output_text = results.raw
        st.markdown(output_text)
        output_buffer = StringIO()
        output_buffer.write(output_text)
        st.download_button(
            label="Download Report",
            data=output_buffer.getvalue(),
            file_name="project_report.md",
            mime="text/markdown"
        )
