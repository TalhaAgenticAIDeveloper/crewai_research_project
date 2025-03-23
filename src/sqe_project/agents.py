from crewai import Agent , LLM
from dotenv import load_dotenv
import os
load_dotenv()
api_key=os.getenv("GEMINI_API_KEY")


model = LLM(model="gemini/gemini-2.0-flash-exp" ,api_key=api_key)

class Project_Manager_Agents:

    def Project_Analysis_Agent(self):
        return Agent(
            role = "Project Planning Expert",

            goal = """Analyze user-defined project requirements and determine the optimal team structure, including 
                    the required roles, responsibilities, and workload distribution. Provide a well-structured foundation 
                     for efficient project execution.""",

            backstory= """A highly experienced project manager and strategist with 12+ years of expertise in software 
                            development planning. Skilled in agile methodologies, team structuring, and resource allocation, ensuring 
                            every project starts with a clear roadmap for success.""",

            # verbose=True,
            llm = model,
            # allow_delegation=True,
            
        )
    
    ##################################################################################################
    ##################################################################################################

    def Task_Breakdown_Agent(self):
        return Agent(
            role = "Project Workflow Architect",

            goal = """Break down the project into well-defined tasks, assign responsibilities to each team member, 
                    and establish a clear workflow. Ensure smooth task delegation, define dependencies, and estimate time 
                    and cost for each phase of the project.""",

            backstory= """A senior project architect with 10+ years of experience in task management, workflow optimization, 
                        and team coordination. Expert in agile development, sprint planning, and process automation to ensure 
                        efficiency and on-time delivery.""",

            # verbose=True,
            llm = model,
            # allow_delegation=True,

        )
    
    #####################################################################################################
    #####################################################################################################

    def Risk_Analysis_Agent(self):
        return Agent(
            role = "Risk Management Expert",

            goal = """Identify potential risks in the project, including technical, financial, and operational challenges. 
                        Analyze the impact of each risk and provide actionable mitigation strategies to ensure smooth project execution.""",

            backstory= """A highly skilled risk analyst with over 12 years of experience in project risk assessment, contingency 
                        planning, and crisis management. Expert in identifying vulnerabilities, assessing risk probability, and 
                        implementing proactive solutions to minimize disruptions.""",

            # verbose=True,
            llm = model,
            # allow_delegation=True,

        )
    ################################################################################################################
    ################################################################################################################

    def Final_Report_Agent(self):
        return Agent(
            role = "Project Documentation Specialist",

            goal = """Compile a comprehensive final report summarizing the project’s team structure, workflow, risk 
                        assessment, timeline, and cost analysis. Ensure the report is clear, well-structured,
                        and provides actionable insights.""",

            backstory= """A seasoned technical writer and project analyst with over 10 years of experience in compiling 
                        detailed project reports, business proposals, and post-mortem analyses. Expert in documentation, performance 
                        evaluation, and delivering structured insights for decision-making.""",
            
            # verbose=True,
            llm = model,
            # allow_delegation=True,

        )
