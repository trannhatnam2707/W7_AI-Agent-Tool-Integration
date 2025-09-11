# main.py
import re
from fastapi import FastAPI
from state import create_state
from agent import plan_and_execute
from config import configure_cors
from models import AskRequest, AskResponse

app = FastAPI(title="Population BE", version="1.0.0")
configure_cors(app)


# ----------------------
# Helpers
# ----------------------
country_mapping = {
    'việt nam': 'vietnam', 'vietnam': 'vietnam', 'viet nam': 'vietnam', 'vn': 'vietnam',
    'china': 'china', 'trung quốc': 'china',
    'nhật bản': 'japan', 'japan': 'japan',
    'hàn quốc': 'south-korea', 'south korea': 'south-korea', 'korea': 'south-korea',
    'thái lan': 'thailand', 'thailand': 'thailand',
    'singapore': 'singapore', 'malaysia': 'malaysia',
    'philippines': 'philippines', 'indonesia': 'indonesia',
    'india': 'india', 'ấn độ': 'india'
}


def extract_country(user_query: str) -> str:
    q = user_query.lower()
    for k, v in country_mapping.items():
        if k in q:
            return v
    return "vietnam"


def extract_years(user_query: str) -> list[int]:
    years = list(map(int, re.findall(r"\b(?:19|20)\d{2}\b", user_query)))
    years.sort()
    return years


# ----------------------
# Routes
# ----------------------
@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):
    try:
        state = create_state()
        user_query = request.query

        # Extract country
        country = extract_country(user_query)
        state["country"] = country

        # Extract years
        years = extract_years(user_query)
        if len(years) >= 2:
            state["year_start"] = years[0]
            state["year_end"] = years[1]
        if len(years) >= 3:
            state["future_year"] = years[2]
        elif len(years) == 2:
            state["future_year"] = years[1] + 5

        # Gọi agent xử lý
        updated_state = plan_and_execute(user_query, state)

        # Soạn câu trả lời ngắn gọn
        parts = []
        if updated_state.get("population_start") and updated_state.get("population_end"):
            parts.append(
                f"Dân số năm {updated_state['year_start']}: {updated_state['population_start']:,}, "
                f"năm {updated_state['year_end']}: {updated_state['population_end']:,}."
            )
        if updated_state.get("growth_rate"):
            parts.append(f"Tốc độ tăng trưởng: {updated_state['growth_rate']*100:.3f}%/năm.")
        if updated_state.get("predicted_population") and updated_state.get("future_year"):
            parts.append(
                f"Dự đoán năm {updated_state['future_year']}: {updated_state['predicted_population']:,}."
            )
        answer = " ".join(parts) if parts else "Không thể lấy đủ dữ liệu để trả lời."

        return AskResponse(
            success=True,
            answer=answer,
            country=updated_state.get("country"),
            year_start=updated_state.get("year_start"),
            year_end=updated_state.get("year_end"),
            future_year=updated_state.get("future_year"),
            population_start=updated_state.get("population_start"),
            population_end=updated_state.get("population_end"),
            growth_rate=updated_state.get("growth_rate"),
            predicted_population=updated_state.get("predicted_population"),
            history=updated_state.get("history", []),
        )
    except Exception as e:
        return AskResponse(success=False, error=str(e))
