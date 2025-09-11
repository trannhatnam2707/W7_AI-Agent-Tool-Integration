import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from tools import translate, synonym
from langgraph.prebuilt import create_react_agent


load_dotenv()  # Load biến môi trường từ file .env

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash", 
    google_api_key=os.getenv("GEMINI_API_KEY")
)

def build_react_agent():
    tools = [translate, synonym]
    return create_react_agent(llm, tools)