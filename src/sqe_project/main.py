from agents import Project_Manager_Agents
from tasks import Project_Manager_Tasks
from crewai import Crew , Process ,LLM
import streamlit as st
from dotenv import load_dotenv
import os


load_dotenv()
api_key=os.getenv("GEMINI_API_KEY")


model = LLM(model="gemini/gemini-2.0-flash-exp" ,api_key=api_key)


############################################################################################
#Taking Inputs
############################################################################################

project_Title = st.text_input("project_Title")

Project_Requirements = st.text_input("Project_Requirements")




############################################################################################
# Creating Objects of Agents and Tasks
############################################################################################

agents = Project_Manager_Agents()
tasks = Project_Manager_Tasks()



############################################################################################
# Imporinting all Agents
############################################################################################

Project_Analysis_Agent = agents.Project_Analysis_Agent()    # Agent 1
Task_Breakdown_Agent = agents.Task_Breakdown_Agent()    # Agent 2
Risk_Analysis_Agent = agents.Risk_Analysis_Agent()      # Agent 3
Final_Report_Agent = agents.Final_Report_Agent()        # Agent 4




# def save_to_markdown(text, filename="output.md"):
#     with open(filename, "w", encoding="utf-8") as file:
#         file.write(text)
#     print(f"Markdown file saved as {filename}")






############################################################################################
# Assigning Tasks to Each Agent
############################################################################################

# Task 1
Project_Analysis_Task = tasks.Project_Analysis_Task(

    agent = Project_Analysis_Agent,

    project_Title = project_Title,
    Project_Requirements = Project_Requirements
)

# Task 2
Task_Breakdown_Task = tasks.Task_Breakdown_Task(
    agent = Task_Breakdown_Agent,
    context = [Project_Analysis_Task],
    # callback = save_to_markdown,

)

# Task 3
Risk_Analysis_Task = tasks.Risk_Analysis_Task(
    agent = Risk_Analysis_Agent,
    context = [Task_Breakdown_Task],
    # callback = save_to_markdown,

)

# Task 4
Final_Report_Task = tasks.Final_Report_Task(
    agent = Final_Report_Agent,
    context = [Risk_Analysis_Task],
    # callback = save_to_markdown,

)





############################################################################################
# Creating Crew here
############################################################################################

crew =  Crew(

    agents=[Content_Strategist, Writer],
    tasks=[Content_Strategist_Task, Writer_Task],
    verbose=True,
    # process = Process.hierarchical,
    # manager_llm = model,

)

action = st.button("submit")
if action:
    with st.spinner("Processing... Please wait"):  # Show loading spinner
        results = crew.kickoff()
        st.write(results)
