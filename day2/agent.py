# agent.py
from dotenv import load_dotenv
import google.generativeai as genai
from tools import get_population_by_year, calculate_growth_rate, predict_population
from langchain_google_genai import ChatGoogleGenerativeAI
from state import log_observation, log_decision, log_action, complete_step
import os
import json, re

load_dotenv()

# --- Khởi tạo Gemini LLM ---
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY")
)


# --- Sinh plan từ LLM ---
def ask_llm_for_plan(user_query: str):
    prompt = f"""
Bạn là một AI Planner. 
Phân tích câu hỏi người dùng và trả về một kế hoạch JSON để thực hiện.

YÊU CẦU:
- Chỉ trả về JSON hợp lệ, không thêm giải thích.
- JSON là một array gồm các bước.
- Mỗi bước có "action" và tham số cần thiết.
- Mỗi action cần tham số "country" nếu liên quan dân số.

Các action hợp lệ:
1. "get_population": lấy dân số của một năm.
   {{ "action": "get_population", "country": "vietnam", "year": 2023 }}
2. "calculate_growth": tính tỉ lệ tăng trưởng.
   {{ "action": "calculate_growth", "start_year": 2023, "end_year": 2025 }}
3. "predict_population": dự đoán dân số.
   {{ "action": "predict_population", "future_year": 2030 }}

Câu hỏi: "{user_query}"
"""
    response = llm.invoke(prompt)
    return response.content.strip()


# --- Thực thi plan ---
def execute_plan(plan_json, state):
    print("\n🚀 Bắt đầu thực hiện kế hoạch...")
    log_observation(state, f"Nhận được plan từ LLM: {plan_json}")

    # Làm sạch JSON (loại bỏ ```json ... ```)
    cleaned = re.sub(r"^```(?:json)?|```$", "", plan_json.strip(), flags=re.IGNORECASE).strip()

    try:
        steps = json.loads(cleaned)
        log_observation(state, f"Parse JSON thành công, có {len(steps)} bước")
    except json.JSONDecodeError as e:
        print(f"❌ Lỗi parse JSON: {e}")
        return state

    for i, step in enumerate(steps, 1):
        action = step["action"]
        print(f"\n📍 Bước {i}/{len(steps)}: {action}")

        # === OBSERVE ===
        log_observation(state, f"Quan sát step {i}: {step}")

        try:
            if action == "get_population":
                # === DECIDE ===
                country = step.get("country", "vietnam")
                year = step["year"]
                log_decision(state, f"Quyết định lấy dân số {country} năm {year}")

                # === ACT ===
                print(f"   🔍 Lấy dân số {country} năm {year}...")
                population = get_population_by_year(country, year)
                print(f"   ✅ Dân số {country} năm {year}: {population:,}")

                # Cập nhật state
                if year == state.get("year_start"):
                    state["population_start"] = population
                elif year == state.get("year_end"):
                    state["population_end"] = population

                log_action(state, f"Lấy dân số {year}: {population:,}")
                complete_step(state, i, f"Dân số {year}: {population:,}")

            elif action == "calculate_growth":
                start_pop = state.get("population_start")
                end_pop = state.get("population_end")
                start_year = step["start_year"]
                end_year = step["end_year"]

                if start_pop is None or end_pop is None:
                    print(f"   ⚠️ Thiếu dữ liệu dân số: start={start_pop}, end={end_pop}")
                    continue

                # === DECIDE ===
                log_decision(state, f"Tính growth rate từ {start_pop:,} đến {end_pop:,} ({start_year}→{end_year})")

                # === ACT ===
                years = end_year - start_year
                growth_rate = calculate_growth_rate(start_pop, end_pop, years)
                state["growth_rate"] = growth_rate
                print(f"   ✅ Growth rate: {growth_rate*100:.3f}%/năm")

                log_action(state, f"Tốc độ tăng trưởng: {growth_rate*100:.3f}%/năm")
                complete_step(state, i, f"Tốc độ tăng trưởng: {growth_rate*100:.3f}%/năm")

            elif action == "predict_population":
                current_pop = state.get("population_end")
                growth_rate = state.get("growth_rate")
                future_year = step["future_year"]
                current_year = state.get("year_end")

                if current_pop is None or growth_rate is None or current_year is None:
                    print(f"   ⚠️ Thiếu dữ liệu: pop={current_pop}, rate={growth_rate}, year={current_year}")
                    continue

                # === DECIDE ===
                log_decision(state, f"Dự đoán dân số {future_year} từ {current_pop:,} với rate {growth_rate:.5f}")

                # === ACT ===
                years_future = future_year - current_year
                predicted = predict_population(current_pop, growth_rate, years_future)
                state["predicted_population"] = predicted
                state["future_year"] = future_year
                print(f"   ✅ Dân số {future_year}: {predicted:,}")

                log_action(state, f"Dự đoán dân số năm {future_year}: {predicted:,}")
                complete_step(state, i, f"Dân số năm {future_year}: {predicted:,}")

            else:
                print(f"   ⚠️ Action không hỗ trợ: {action}")
                log_action(state, f"Action không hỗ trợ: {action}")
                complete_step(state, i, "failed")

        except Exception as e:
            print(f"   ❌ Lỗi tại bước {i}: {e}")
            log_observation(state, f"Lỗi step {i}: {e}")

    print("\n✅ Hoàn thành thực hiện kế hoạch!")
    return state


# --- Tổng hợp: Plan + Execute ---
def plan_and_execute(user_query, state):
    print("\n🤖 Đang tạo kế hoạch từ LLM...")
    plan_json = ask_llm_for_plan(user_query)
    print("📋 Plan LLM sinh ra:")
    print(plan_json)
    print("-" * 50)

    updated_state = execute_plan(plan_json, state)
    return updated_state
