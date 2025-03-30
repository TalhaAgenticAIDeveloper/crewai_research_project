from crewai import  Task
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
import os 
load_dotenv()


os.getenv("GEMINI_API_KEY")

research_tool = SerperDevTool()

class Project_Manager_Tasks():

##############################################################################################################
    # Task 1
##############################################################################################################
    
    def Project_Analysis_Task(self, agent, project_Title, Project_Requirements, further_context):
        return Task(
            description=f"""Analyze the user-defined project '{project_Title}' by reviewing its initial and enhanced requirements. 

            The agent will:
            - Evaluate the given project requirements: {Project_Requirements}
            - Incorporate additional enhancements from previous analysis: {further_context}
            - Determine the necessary team structure and skill sets required.

            Parameters:
            - Project Title: {project_Title}
            - Initial Requirements: {Project_Requirements}
            - Enhanced Requirements from previous analysis: {further_context}

            The agent will analyze the complexity and scope of the project, 
            identify the required team roles (frontend developers, backend developers, UI/UX designers, testers, project managers, etc.), 
            and estimate the ideal team size.
            """,
            
            tools=[],
            agent=agent,
            expected_output="A structured report detailing the required team composition, skill set, and estimated team size."
    )


##############################################################################################################
    # Task 2
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
    # Task 3
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
    # Task 4
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

