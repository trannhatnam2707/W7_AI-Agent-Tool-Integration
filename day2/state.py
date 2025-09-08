def create_state():
    """Tạo và trả về một từ điển (dictionary) để lưu trữ trạng thái của chương trình.
    Các khóa được khởi tạo với giá trị None, sẵn sàng để được điền dữ liệu."""
    
    return {
        "year_start": None,
        "year_end": None,
        "population": None,
        "population_end": None,
        "growth_rate": None,
        "future_year": None,
        "predicted_population": None,
    }
