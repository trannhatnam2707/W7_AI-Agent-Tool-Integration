import requests, re
from bs4 import BeautifulSoup

# tool1: lấy dữ liệu dân số từ worldometer
def get_population_by_year(country: str, year: int):
    url = f"https://www.worldometers.info/world-population/{country.lower()}-population/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"} 
    
    print(f"      🌐 Đang truy cập: {url}")
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = "utf-8"
        if response.status_code != 200:
            raise Exception(f"Failed to fetch data for {country}. Status code: {response.status_code}")
    except requests.RequestException as e:
        raise Exception(f"Network error when fetching data for {country}: {e}")
    
    soup = BeautifulSoup(response.text, 'html.parser')

    # Tìm heading phía trên bảng dân số - cải thiện tìm kiếm
    possible_headings = [
        f"Population of {country.capitalize()}",
        f"{country.capitalize()} Population",
        f"Historical Population of {country.capitalize()}",
        "Historical Population"
    ]
    
    h2 = None
    for heading_text in possible_headings:
        h2 = soup.find(lambda tag: tag.name in ["h1", "h2", "h3"] and heading_text.lower() in tag.get_text().lower())
        if h2:
            print(f"      ✅ Tìm thấy heading: {h2.get_text().strip()}")
            break
    
    if not h2:
        # Thử tìm bảng trực tiếp
        print(f"      ⚠️  Không tìm thấy heading, thử tìm bảng trực tiếp...")
        tables = soup.find_all("table")
        for table in tables:
            if table.find("th") and "year" in table.get_text().lower():
                print(f"      ✅ Tìm thấy bảng có thể chứa dữ liệu dân số")
                return extract_population_from_table(table, year, country)
        
        raise RuntimeError(f"Could not find population data for {country}")

    # Tìm bảng ngay sau heading
    table = h2.find_next("table")
    if not table:
        # Thử tìm bảng gần nhất
        table = h2.find_parent().find_next("table")
        if not table:
            raise RuntimeError(f"Could not find table after heading for {country}")
    
    return extract_population_from_table(table, year, country)

def extract_population_from_table(table, year, country):
    """Trích xuất dân số từ bảng HTML"""
    print(f"      🔍 Tìm kiếm năm {year} trong bảng...")
    
    # Duyệt qua các hàng của bảng để tìm năm trùng
    rows_found = 0
    for tr in table.find_all("tr"):
        cols = [td.get_text(" ", strip=True) for td in tr.find_all(["td", "th"])]
        if len(cols) < 2:
            continue
            
        rows_found += 1
        year_str = cols[0].strip()
        
        # In ra một vài hàng đầu để debug
        if rows_found <= 5:
            print(f"      📄 Hàng {rows_found}: {cols[:3]}")  # In 3 cột đầu
        
        if year_str == str(year):
            pop_text = cols[1] if len(cols) > 1 else ""
            print(f"      🎯 Tìm thấy năm {year}: {pop_text}")
            
            # Làm sạch text và chỉ lấy số
            pop_digits = re.sub(r"[^\d]", "", pop_text)
            if pop_digits:
                population = int(pop_digits)
                print(f"      ✅ Dân số năm {year}: {population:,}")
                return population
            else:
                print(f"      ❌ Không thể parse số từ: {pop_text}")
    
    print(f"      📊 Tổng cộng đã kiểm tra {rows_found} hàng")
    raise RuntimeError(f"Could not find population data for {country} in year {year}")

# tool 2: tính tỷ lệ tăng trưởng hàng năm - SỬA LẠI CÔNG THỨC  
def calculate_growth_rate(start_pop, end_pop, years):
    """
    Tính tốc độ tăng trưởng dân số trung bình hàng năm
    Sử dụng công thức: ((end/start)^(1/years)) - 1
    """
    if start_pop <= 0 or end_pop <= 0 or years <= 0:
        raise ValueError("Tất cả tham số phải lớn hơn 0")
    
    # Công thức compound annual growth rate (CAGR)
    growth_rate = ((end_pop / start_pop) ** (1 / years)) - 1
    
    print(f"      📊 Tính toán: ({end_pop:,} / {start_pop:,}) ^ (1/{years}) - 1 = {growth_rate:.6f}")
    
    return growth_rate

# tool 3: Dự đoán dân số trong tương lai - SỬA LẠI CÔNG THỨC
def predict_population(current_pop, annual_growth_rate, years):
    """
    Dự đoán dân số tương lai với công thức compound growth
    Formula: future_pop = current_pop * (1 + rate)^years
    """
    if current_pop <= 0 or years < 0:
        raise ValueError("current_pop phải > 0, years phải >= 0")
    
    future_population = current_pop * ((1 + annual_growth_rate) ** years)
    
    print(f"    🔮 Dự đoán: {current_pop:,} * (1 + {annual_growth_rate:.6f})^{years} = {int(future_population):,}")
    
    return int(future_population)