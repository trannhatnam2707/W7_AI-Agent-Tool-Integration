# agent.py
from dotenv import load_dotenv
import google.generativeai as genai
from tools import get_population_by_year, calculate_growth_rate, predict_population
from langchain_google_genai import ChatGoogleGenerativeAI
import os


load_dotenv()   

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash", 
    google_api_key=os.getenv("GEMINI_API_KEY")
)


def ask_llm_for_plan(user_query: str):
    prompt = f"""
    Bạn là AI Agent theo kiến trúc Plan-and-Execute.
    Nhiệm vụ: từ câu hỏi của người dùng, hãy lập KẾ HOẠCH bằng JSON.
    Kế hoạch cần có dạng:
    [
      {{"action": "get_population", "year": 2015}},
      {{"action": "get_population", "year": 2020}},
      {{"action": "calculate_growth", "start_year": 2015, "end_year": 2020}},
      {{"action": "predict_population", "future_year": 2030}}
    ]

    Câu hỏi người dùng: {user_query}
    """
    response = llm.invoke(prompt)
    return response.content

def execute_plan(plan_json, state):
    import json, re
    
    # loại bỏ ```json và ```
    cleaned = plan_json.strip()
    cleaned = re.sub(r"^```json", "", cleaned, flags=re.IGNORECASE).strip()
    cleaned = re.sub(r"^```", "", cleaned).strip()
    cleaned = re.sub(r"```$", "", cleaned).strip()

    steps = json.loads(cleaned)

    for step in steps:
        action = step["action"]

        if action == "get_population":
            year = step["year"]
            population = get_population_by_year(year)
            if year == state["year_start"]:
                state["population_start"] = population
            elif year == state["year_end"]:
                state["population_end"] = population

        elif action == "calculate_growth":
            start = state["population_start"]
            end = state["population_end"]
            years = step["end_year"] - step["start_year"]
            state["growth_rate"] = calculate_growth_rate(start, end, years)

        elif action == "predict_population":
            years_future = step["future_year"] - state["year_end"]
            state["predicted_population"] = predict_population(
                state["population_end"], state["growth_rate"], years_future
            )

    return state



def plan_and_execute(user_query, state):
    plan_json = ask_llm_for_plan(user_query)
    print("Plan mà LLM sinh ra:\n", plan_json)
    updated_state = execute_plan(plan_json, state)
    return updated_state
