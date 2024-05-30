from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse,RedirectResponse
from crewai import Agent
from tools import tool
from dotenv import load_dotenv
import os
from crewai import Task
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai import Crew, Process

app = FastAPI()

# Load environment variables
load_dotenv()


# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    verbose=True,
    temperature=0.5,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Initialize stock analysis agent
stock_analysis_agent = Agent(
    role="Financial Analyst",
    goal="Provide a comprehensive analysis of the stock for a specific company, including financial metrics, news sentiment, and technical indicators, to determine investment recommendations.",
    verbose=True,
    memory=True,
    backstory=(
        "As an experienced financial analyst, you are dedicated to thoroughly examining company stocks."
        " You leverage financial data, news sentiment, and technical analysis to offer informed investment"
        " recommendations to users."
    ),
    tools=[tool],
    llm=llm,
    allow_delegation=True
)

# Define research task
stock_analysis_task = Task(
    description=(
        "Perform a comprehensive analysis of the stock for the company {CompanyName}. This includes extracting and analyzing financial metrics, news sentiment, and technical indicators to provide an investment recommendation."
    ),
    expected_output=(
        "Provide a detailed investment recommendation for the company {CompanyName} based on financial data, news sentiment, and technical indicators. Include reasons for the recommendation."
    ),
    tools=[tool],
    agent=stock_analysis_agent,
    output_file='Advice.md'
)

# Initialize crew
crew = Crew(
    agents=[stock_analysis_agent],
    tasks=[stock_analysis_task],
    process=Process.sequential,
)

@app.get("/", response_class=RedirectResponse)
async def read_root():
    return RedirectResponse(url="/docs")

@app.post("/Analyze Stock/", response_class=JSONResponse)
async def analyze_stock(CompanyName: str = Form(...)):
    result = crew.kickoff(inputs={"CompanyName": CompanyName})
    return {"result": result}
