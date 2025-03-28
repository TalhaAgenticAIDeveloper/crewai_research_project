from agents import Project_Manager_Agents
from tasks import Project_Manager_Tasks
from crewai import Crew , Process ,LLM
import streamlit as st
import markdown
from dotenv import load_dotenv
from io import StringIO
import os
import re

load_dotenv()
api_key=os.getenv("GEMINI_API_KEY")


# model = LLM(model="gemini/gemini-2.0-flash-exp" ,api_key=api_key)


############################################################################################
#Taking Inputs
############################################################################################

project_Title = st.text_input("Project Title")

Project_Requirements = st.text_input("Project Requirements")




############################################################################################
# Creating Objects of Agents and Tasks
############################################################################################

agents = Project_Manager_Agents()
tasks = Project_Manager_Tasks()



############################################################################################
# Imporinting all Agents
############################################################################################

Missing_Requirements_Agent = agents.Missing_Requirements_Agent()    # Agent 1
Project_Analysis_Agent = agents.Project_Analysis_Agent()    # Agent 2
Task_Breakdown_Agent = agents.Task_Breakdown_Agent()    # Agent 3
Risk_Analysis_Agent = agents.Risk_Analysis_Agent()      # Agent 4
Final_Report_Agent = agents.Final_Report_Agent()        # Agent 5



############################################################################################
# Assigning Tasks to Each Agent
############################################################################################

# Task 1
Missing_Requirements_Task = tasks.Missing_Requirements_Task(

    agent = Missing_Requirements_Agent,

    project_Title = project_Title,
    Project_Requirements = Project_Requirements
)


# Task 2
Project_Analysis_Task = tasks.Project_Analysis_Task(

    agent = Project_Analysis_Agent,

    project_Title = project_Title,
    Project_Requirements = Project_Requirements,
    context = [Missing_Requirements_Task]
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





############################################################################################
# Creating Crew here
############################################################################################

crew =  Crew(

    agents=[Project_Analysis_Agent, Task_Breakdown_Agent, Risk_Analysis_Agent, Final_Report_Agent],
    tasks=[Project_Analysis_Task, Task_Breakdown_Task, Risk_Analysis_Task, Final_Report_Task],
    verbose=True,

)




def save_output_to_markdown(output, filename="agent_output.md"):
    """Saves the output in a structured Markdown file."""
    with open(filename, "w", encoding="utf-8") as file:
        # file.write("# Agent Output\n\n")  # Main heading
        file.write(output.replace("**", "")) 



# Button for Processing
if st.button("Submit"):
    with st.spinner("Processing... Please wait"):
        results = crew.kickoff()
        # output_text = results.raw  # Storing the result
        output_text = results.raw
        # Display Output
        st.markdown(output_text)
        

        # Convert output into a downloadable file
        output_buffer = StringIO()
        output_buffer.write(output_text)

        # Download Button
        st.download_button(
            label="Download Report",
            data=output_buffer.getvalue(),
            file_name="project_report.md",
            mime="text/markdown"
        )
