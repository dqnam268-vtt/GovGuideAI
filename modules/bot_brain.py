import json
import os
import requests
import glob

# Link Google Apps Script
GOOGLE_APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzi8UZVwXnrY_8AEBnwbLUAxEAz6xzeDAJP24kO8wBd9c5g0mdmhx6Qpg0JQkNJuCOg/exec"

def load_knowledge():
    """Quét và nạp tất cả thành phần kiến thức từ thư mục knowledge_base."""
    knowledge_dir = os.path.join(os.path.dirname(__file__), '..', 'knowledge_base')
    combined_data = {
        "thu_tuc": "Các thủ tục Hành chính công",
        "intents": []
    }
    
    # Tìm tất cả file .json
    json_files = glob.glob(os.path.join(knowledge_dir, '*.json'))
    
    for file_path in json_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Kiểm tra và lấy danh sách intents an toàn
                intents = data.get('intents', [])
                if isinstance(intents, list):
                    combined_data['intents'].extend(intents)
        except Exception as e:
            print(f"Lỗi khi đọc tệp {file_path}: {e}")
            continue
            
    return combined_data

def get_response(user_message):
    """Thuật toán RAG: Tích hợp an toàn với dữ liệu JSON và Gemini API."""
    data = load_knowledge()
    
    if not data or not data['intents']:
        return "Xin lỗi, hệ thống dữ liệu chưa được nạp. Vui lòng kiểm tra lại các tệp JSON."

    # 1. Trích xuất kiến thức an toàn (Sử dụng .get() để tránh KeyError)
    context_text = ""
    for intent in data['intents']:
        # Chỉ lấy những intent có chứa khóa 'response'
        response_content = intent.get('response')
        if response_content:
            context_text += f"- Quy định: {response_content}\n"
    
    # 2. Xây dựng System Prompt
    system_prompt = f"""Bạn là Trợ lý Ảo Hành chính công của Phường Sài Gòn.
    [THÀNH PHẦN KIẾN THỨC CẤP PHÉP]
    {context_text}
    
    [QUY TẮC BẮT BUỘC]
    1. Trả lời DỰA TRÊN THÔNG TIN ở mục [THÀNH PHẦN KIẾN THỨC CẤP PHÉP].
    2. Không tự bịa thông tin. Nếu không có trong kiến thức, nói: "Tôi xin gợi ý bạn liên hệ trực tiếp Bộ phận Một cửa để được hỗ trợ chuyên sâu."
    3. Trình bày thân thiện, mạch lạc.
    4. Cuối câu trả lời luôn ghi: "💡 Gợi ý: Bạn có thể nộp hồ sơ trực tuyến tại [Cổng DVC Quốc Gia](https://dichvucong.gov.vn/) để tiết kiệm thời gian."
    """

    # 3. Gửi Payload
    payload = {
        "action": "solve",
        "contents": [{"parts": [{"text": user_message}]}],
        "systemInstruction": {"parts": [{"text": system_prompt}]}
    }

    try:
        response = requests.post(GOOGLE_APPS_SCRIPT_URL, json=payload, timeout=15)
        response.raise_for_status()
        response_data = response.json()
        
        # Bóc tách an toàn đường dẫn JSON phản hồi
        candidates = response_data.get("candidates", [])
        if candidates:
            bot_text = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "")
            return bot_text if bot_text else "Hệ thống phản hồi trống."
        return "Hệ thống không tìm thấy câu trả lời phù hợp."
            
    except Exception as e:
        return f"Lỗi kết nối máy chủ: {str(e)}"