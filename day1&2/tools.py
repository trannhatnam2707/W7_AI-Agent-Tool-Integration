import os
from dotenv import load_dotenv
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
import requests

load_dotenv() # Load biến môi trường từ file .env


llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",   # hoặc gemini-1.5-pro
    google_api_key=os.getenv("GEMINI_API_KEY")
)

@tool
def translate(word: str) -> str:
    """Dịch từ tiếng Anh sang tiếng Việt"""
    prompt = f"Dịch từ '{word}' sang tiếng Việt." 
    response = llm.invoke(prompt)
    return response.content

@tool
def synonym(word: str) -> str:
    """Tìm từ đồng nghĩa trong tiếng Anh (dùng Datamuse API)"""
    url = f"https://api.datamuse.com/words?ml={word}"
    try:
        res = requests.get(url)
        data = res.json()
        syns = [item['word'] for item in data[:5]] # Lấy 5 từ đồng nghĩa đầu tiên
        return ", ".join(syns) if syns else "Không tìm thấy từ đồng nghĩa." 
    except Exception as e:
        return f"Đã có lỗi xảy ra khi gọi API: {e}"


