# main.py
from state import create_state
from agent import plan_and_execute

def main():
    state = create_state()
    user_query = input("Nhập yêu cầu của bạn: ")

    # Extract năm từ input đơn giản (có thể dùng regex)
    import re
    years = list(map(int, re.findall(r"\d{4}", user_query)))
    if len(years) >= 2:
        state["year_start"] = years[0]
        state["year_end"] = years[1]
    if len(years) >= 3:
        state["future_year"] = years[2]

    updated_state = plan_and_execute(user_query, state)

    print("\n📊 Kết quả:")
    print(f"Dân số {updated_state['year_start']}: {updated_state['population_start']:,}")
    print(f"Dân số {updated_state['year_end']}: {updated_state['population_end']:,}")
    print(f"Tốc độ tăng trưởng trung bình hằng năm: {updated_state['growth_rate']*100:.2f}%")

    if updated_state["future_year"]:
        print(f"Dự đoán dân số năm {updated_state['future_year']}: {updated_state['predicted_population']:,}")

if __name__ == "__main__":
    main()
