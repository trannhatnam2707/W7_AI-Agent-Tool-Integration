import requests
from bs4 import BeautifulSoup

#tool1: lấy dữ liệu dân số từ worldometer
def get_population_by_year(year: int):
    url = "https://www.worldometers.info/world-population/vietnam-population/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table", class_="table table-striped table-bordered table-hover table-condensed table-list") 
    if not table:
        raise ValueError("❌ Không tìm thấy bảng dân số trên trang, có thể HTML đã thay đổi.")

    rows = table.find_all("tr")
    for row in rows:
        cols = row.find_all("td")
        if len(cols) > 0:
            year_text = cols[0].text.strip()
            if year_text == str(year):
                population_text = cols[1].text.strip().replace(",", "")
                return int(population_text)

    return None


#tool 2: tính tỷ lệ tăng trưởng hàng năm
def calculate_growth_rate(start, end, years):
    return (end-start)/(start*years)

#tool 3 :Dự đoán dân số trong tương lai
def predict_population(current_pop, rate, years):
    return int(current_pop *((1+rate)** years))

