from crewai import Agent
from tools import tool
from dotenv import load_dotenv
load_dotenv()
import os
from langchain_google_genai import ChatGoogleGenerativeAI

os.environ['SERPER_API_KEY'] = os.getenv('SERPER_API_KEY')


from crewai_tools import SerperDevTool

# over here we are using gemini model we can use use google palm over here
llm=ChatGoogleGenerativeAI(model="gemini-.15-flash",
                           verbose=True,
                           temperature=0.5,
                           google_api_key=os.getenv("GOOGLE_API_KEY"))

tool  = SerperDevTool()



stock_analysis_agent =Agent(
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

