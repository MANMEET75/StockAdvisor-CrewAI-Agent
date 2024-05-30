from crewai import Crew,Process

from tasks import stock_analysis_task
from agents import stock_analysis_agent

# Creating the crew over here
crew=Crew(
    agents=[stock_analysis_agent],
    tasks=[stock_analysis_task],
    process=Process.sequential,
)

# Starting the task execution process with enhanced feedback over here
result=crew.kickoff(inputs={"topic":"Dell"})
print(result)

