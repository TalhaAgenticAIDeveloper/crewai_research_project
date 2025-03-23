from crewai import  Task
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
import os 
load_dotenv()


os.getenv("GEMINI_API_KEY")

research_tool = SerperDevTool()

class BookWriterTasks():


    def Project_Analysis_Task(self, agent, Project_Title, Requirements):
        return Task(
            description=f"""Analyze the user-defined project '{Project_Title}' by reviewing its requirements and 
                determining the necessary team structure.
                
                Parameters:
                - Project Title: {Project_Title}
                - Requirements: {Requirements}

                The agent will evaluate the project's complexity and suggest the required roles (frontend developers, 
                backend developers, UI/UX designers, testers, project managers, etc.).
            """,
        
            tools = [],
            agent = agent,
            expected_output = "A structured report detailing the required team composition and estimated team size."
    )
    

    ##############################################################################################################
    ##############################################################################################################

    def Task_Breakdown_Task(self, agent, context):
        return Task(
            description=f"""Break down the project into specific tasks based on the provided team structure.
                The agent will define the sequence of tasks, assign responsibilities to each team member, and create a task 
                dependency flowchart.
                """,
            context = context,
            tools = [research_tool],  # Fetch real-time cost and time estimates
            agent = agent,
            expected_output = "A detailed work breakdown structure (WBS) with task dependencies, estimated time, and assigned roles."
    )


    ##############################################################################################################
    ##############################################################################################################

    def Risk_Analysis_Task(self, agent, context):
        return Task(
            description = f"""Perform a risk analysis for the project based on the provided work breakdown structure.
            
                Context from previous agent:
                {context}

                The agent will identify risks related to time delays, resource shortages, technology limitations, and 
                budget overruns, and suggest mitigation strategies.
                """,
            context = context,
            tools = [research_tool],  # Fetch real-world risk data
            agent = agent,
            expected_output = "A comprehensive risk assessment report detailing all possible risks and their mitigation strategies."
    )


    ##############################################################################################################
    ##############################################################################################################


    def Final_Report_Task(self, agent, context):
        return Task(
            description = f"""Compile the final project report summarizing all aspects, including team composition, work 
                breakdown, risk analysis, and cost evaluation.
                
                Context from previous agent:
                {context}

                The agent will structure the final report with all necessary sections, ensuring clarity and completeness.
                """,

            context = context,
            tools = [],
            agent = agent,
            expected_output = "A professionally formatted final project report covering all essential project insights."
    )

