from crewai import Agent, Task, Crew, Process
import os

# Set your API keys (replace with your actual keys)
import data_info

os.environ['OPENAI_API_KEY'] = data_info.open_ai_key  # Replace with your OpenAI API key
#os.environ["GOOGLE_API_KEY"] = "YOUR_GOOGLE_API_KEY" # Optional, if you want Google Search

# Define your agents
editor = Agent(
    role="Editor",
    goal="Oversee the entire news publishing process, ensuring quality and accuracy.",
    backstory="A seasoned editor with decades of experience in journalism.",
    verbose=True,
    allow_delegation=True,
)

reporter = Agent(
    role="Reporter",
    goal="Gather accurate and timely information on assigned topics.",
    backstory="A dedicated journalist with a knack for finding the truth.",
    verbose=True,
    allow_delegation=True,
)

fact_checker = Agent(
    role="Fact Checker",
    goal="Verify the accuracy of all information before publication.",
    backstory="A meticulous fact-checker with a strong eye for detail.",
    verbose=True,
    allow_delegation=False,
)

copy_editor = Agent(
    role="Copy Editor",
    goal="Ensure the article is grammatically correct and stylistically consistent.",
    backstory="A skilled copy editor with a passion for clear and concise writing.",
    verbose=True,
    allow_delegation=False,
)

seo_expert = Agent(
    role="SEO Expert",
    goal="Optimize the article for search engines to maximize visibility.",
    backstory="An experienced SEO specialist with a deep understanding of search engine algorithms.",
    verbose=True,
    allow_delegation=False,
)

publisher = Agent(
    role="Publisher",
    goal="Publish the finalized article on the website.",
    backstory="A website administrator with expertise in content management systems.",
    verbose=True,
    allow_delegation=False,
)


# Define your tasks
report_task = Task(
    description="Write a detailed news report on the following topic: Role of AI in automation.",
    agent=reporter,
    expected_output="A detailed news report in a clear and concise style.", # Add this line
)

fact_check_task = Task(
    description="Verify the accuracy of the report written by the reporter.",
    agent=fact_checker,
    context=[report_task],
    expected_output="A list of verified facts and any inaccuracies found.", # Added expected_output
)

copy_edit_task = Task(
    description="Copy edit the report for grammar, style, and clarity.",
    agent=copy_editor,
    context=[fact_check_task],
    expected_output="The revised report with corrected grammar and improved style.", #Added expected_output
)

seo_task = Task(
    description="Optimize the article for search engines, including keywords, meta descriptions, and internal linking.",
    agent=seo_expert,
    context=[copy_edit_task],
    expected_output="The optimized article with SEO elements added.", #Added expected_output
)

publish_task = Task(
    description="Publish the finalized article on the website.",
    agent=publisher,
    context=[seo_task],
    expected_output="Confirmation that the article has been published.", #Added expected_output
)

review_task = Task(
    description = "Review all aspects of the article and provide a final approval for publication.",
    agent = editor,
    context = [publish_task],
    expected_output = "A final approval or list of required changes.", #Added expected_output
)

# Create the crew
newspaper_crew = Crew(
    agents=[editor, reporter, fact_checker, copy_editor, seo_expert, publisher],
    tasks=[report_task, fact_check_task, copy_edit_task, seo_task, publish_task, review_task],
    verbose=True, # You can set it to 1 or 2 to different logging levels
    process=Process.sequential,  # Tasks are executed in a sequence
)

# Run the crew
result = newspaper_crew.kickoff()

print("\nFinal Result:")
print(result)
