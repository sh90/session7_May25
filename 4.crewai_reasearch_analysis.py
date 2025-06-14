#####
## Sequential but dependent execution
####
from crewai import Agent, Task, Crew, Process
import data_info
import os

os.environ['OPENAI_API_KEY'] = data_info.open_ai_key

# Define agents
researcher = Agent(
    role='Researcher',
    goal='Conduct thorough research on a given topic',
    backstory='An expert analyst with a knack for detailed insights',

)

writer = Agent(
    role='Writer',
    goal='Write compelling content using research',
    backstory='A skilled writer passionate about storytelling'
)

# Define tasks
research_task = Task(
    description='Investigate the latest trends in {topic}.',
    agent=researcher,
    expected_output='A comprehensive research report with sources.'
)

write_task = Task(
    description='Write a blog post about based on the research findings.',
    agent=writer,
    context=[research_task],  # uses the output of research_task internally
    expected_output='An engaging blog post written in markdown format.'
)

# Assemble the crew
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process=Process.sequential
)

# Run the crew with inputs
result = crew.kickoff(inputs={'topic': 'Quantum Computing'})
print(result.raw)  # .raw gives the raw output string
