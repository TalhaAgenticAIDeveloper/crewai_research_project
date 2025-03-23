from agents import BookWriterAgents
from tasks import BookWriterTasks
from crewai import Crew , Process ,LLM
import streamlit as st
from dotenv import load_dotenv
import os



load_dotenv()
api_key=os.getenv("GEMINI_API_KEY")


model = LLM(model="gemini/gemini-2.0-flash-exp" ,api_key=api_key)

# var

word_count = st.text_input("word_count")

Book_Title = st.text_input("Book_Title")

Author_Name = st.text_input("Author_Name")

Target_Audience = st.text_input("Target_Audience")

Writing_Style = st.text_input("Writing_Style")


# obj

agents = BookWriterAgents()
tasks = BookWriterTasks()


# Agents

Content_Strategist = agents.Content_Strategist()
Writer = agents.Writer()

# Tasks


Content_Strategist_Task = tasks.Content_Strategist_Task(
    agent = Content_Strategist,
    word_count = word_count,
    Book_Title = Book_Title,
    Author_Name = Author_Name,
    Target_Audience = Target_Audience,
    Writing_Style = Writing_Style,
)


def save_to_markdown(text, filename="output.md"):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(text)
    print(f"Markdown file saved as {filename}")



Writer_Task = tasks.Writer_Task(
    agent = Writer,
    context = [Content_Strategist_Task],
    callback = save_to_markdown,

)





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
