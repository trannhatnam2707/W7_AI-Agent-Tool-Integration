# main.py
from state import create_state
from agent import plan_and_execute
import re

def extract_country_from_query(user_query):
    """Trích xuất tên quốc gia từ câu hỏi người dùng"""
    query_lower = user_query.lower()
    
    # Mapping các cách gọi tên quốc gia phổ biến
    country_mapping = {
        'việt nam': 'vietnam',
        'vietnam': 'vietnam', 
        'viet nam': 'vietnam',
        'vn': 'vietnam',
        'china': 'china',
        'trung quốc': 'china',
        'nhật bản': 'japan',
        'japan': 'japan',
        'hàn quốc': 'south-korea',
        'south korea': 'south-korea',
        'korea': 'south-korea',
        'thái lan': 'thailand',
        'thailand': 'thailand',
        'singapore': 'singapore',
        'malaysia': 'malaysia',
        'philippines': 'philippines',
        'indonesia': 'indonesia',
        'india': 'india',
        'ấn độ': 'india'
    }
    
    # for key, value in country_mapping.items():
    #     if key in query_lower:
    #         print(f"   🎯 Tìm thấy '{key}' -> '{value}'")
    #         return value
    
    # # Mặc định là vietnam nếu không tìm thấy
    # print(f"   ⚠️  Không tìm thấy quốc gia cụ thể, dùng mặc định: vietnam")
    # return 'vietnam'

def main():
    state = create_state()
    user_query = input("Nhập yêu cầu của bạn: ")
    
    print(f"📝 Câu hỏi: {user_query}")
    print("=" * 60)

    # Extract quốc gia từ input
    country = extract_country_from_query(user_query)
    state["country"] = country
    print(f"🌍 Quốc gia được xác định: {country}")

    # Extract năm từ input đơn giản (có thể dùng regex)
    years = list(map(int, re.findall(r"\b(?:19|20)\d{2}\b", user_query)))
    years.sort()  # Sắp xếp theo thứ tự tăng dần
    
    print(f"📅 Các năm được tìm thấy: {years}")
    
    if len(years) >= 2:
        state["year_start"] = years[0]
        state["year_end"] = years[1]
        print(f"📅 Năm bắt đầu: {years[0]}, Năm kết thúc: {years[1]}")
    
    if len(years) >= 3:
        state["future_year"] = years[2]
        print(f"🔮 Năm dự đoán: {years[2]}")
    elif len(years) == 2:
        # Nếu chỉ có 2 năm, có thể user muốn dự đoán thêm vài năm nữa
        state["future_year"] = years[1] + 5  # Mặc định dự đoán thêm 5 năm
        print(f"🔮 Năm dự đoán mặc định: {state['future_year']}")

    updated_state = plan_and_execute(user_query, state)

    print("\n" + "="*60)
    print("📊 KẾT QUẢ CUỐI CÙNG:")
    print("="*60)
    
    if updated_state.get('population_start') and updated_state.get('population_end'):
        print(f"🏙️  Dân số năm {updated_state['year_start']}: {updated_state['population_start']:,}")
        print(f"🏙️  Dân số năm {updated_state['year_end']}: {updated_state['population_end']:,}")
        
        if updated_state.get('growth_rate'):
            print(f"📈 Tốc độ tăng trưởng trung bình: {updated_state['growth_rate']*100:.3f}%/năm")
        
        if updated_state.get("predicted_population") and updated_state.get("future_year"):
            print(f"🔮 Dự đoán dân số năm {updated_state['future_year']}: {updated_state['predicted_population']:,}")
    else:
        print("⚠️  Không thể lấy được dữ liệu đầy đủ")
    
    # In ra lịch sử thực hiện
    if updated_state.get("history"):
        print("\n📜 LỊCH SỬ THỰC HIỆN:")
        for i, record in enumerate(updated_state["history"], 1):
            print(f"   {i}. {record.get('result', 'N/A')}")

if __name__ == "__main__":
    main()