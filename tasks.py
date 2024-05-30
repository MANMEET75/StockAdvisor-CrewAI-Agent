from crewai import Task
from tools import tool
from agents import stock_analysis_agent

# Research task
stock_analysis_task = Task(
    description=(
        "Perform a comprehensive analysis of the stock for the company {topic}. This includes extracting and analyzing financial metrics, news sentiment, and technical indicators to provide an investment recommendation."
    ),
    expected_output=(
        "Provide a detailed investment recommendation for the company {topic} based on financial data, news sentiment, and technical indicators. Include reasons for the recommendation."
    ),
    tools=[tool],
    agent=stock_analysis_agent,
    output_file='Advice.md'
)

