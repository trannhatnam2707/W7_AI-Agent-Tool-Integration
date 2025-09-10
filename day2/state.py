def create_state():
    """Tạo và trả về một từ điển (dictionary) để lưu trữ trạng thái của chương trình.
    Các khóa được khởi tạo với giá trị None, sẵn sàng để được điền dữ liệu."""
    
    return {
        # Input từ người dùng
        "country": None,
        "year_start": None,
        "year_end": None,
        "future_year": None,
        
        # Dữ liệu lấy từ website
        "population_start": None,
        "population_end": None,
        "growth_rate": None,
        "predicted_population": None,
        
        #Quản lý trạng thái của plan do llm sinh ra
        "plan": [],
        "current_step": 0,
        "plan_version": [], 
        "decisions": [],
        "observations": [],
        "actions": [],
        "history": []  # Lịch sử các bước đã hoàn thành
    }

#Các hàm helper để thao tác với state
def update_plan(state:dict, new_plan: list):
    """Cập nhật plan mới và lưu plan cũ"""
    if state["plan"]:
        state["plan_version"].append(state["plan"].copy()) # Lưu plan cũ vào lịch sử
    state["plan"] = new_plan
    state["current_step"] = 1 # Reset current_step khi có plan mới 

def log_observation(state, obs):
    state["observations"].append(obs)
    print("Observation:", obs)

def log_decision(state, decision):
    state["decisions"].append(decision)
    print("Decision:", decision)

def log_action(state, action):
    state["actions"].append(action)
    print("Action:", action)

def complete_step(state:dict, step: int, result: str):
    """Đánh dấu 1 bước đã hoàn thành và log kết quả """
    found = False
    for p in state["plan"]:
        if p["step"] == step:
            p["result"] = result
            state["history"].append({"step": step, "result": result})
            state["current_step"] += 1
            found = True
            break
    
    if not found:
        state["history"].append({"step": step, "action": "unknown step", "result": result})
        state["current_step"] += 1
        