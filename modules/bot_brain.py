import json
import os
import requests

# Link Google Apps Script từ file index của bạn
GOOGLE_APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzi8UZVwXnrY_8AEBnwbLUAxEAz6xzeDAJP24kO8wBd9c5g0mdmhx6Qpg0JQkNJuCOg/exec"

def load_knowledge():
    """Nạp thành phần kiến thức từ các file JSON."""
    knowledge_path = os.path.join(os.path.dirname(__file__), '..', 'knowledge_base', '01_khai_sinh.json')
    try:
        with open(knowledge_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        return None

def get_response(user_message):
    """Thuật toán RAG: Kết hợp dữ liệu JSON và Gemini API qua Google Apps Script."""
    data = load_knowledge()
    
    if not data:
        return "Xin lỗi, hệ thống dữ liệu cục bộ đang được bảo trì. Vui lòng thử lại sau."

    # 1. Trích xuất thành phần kiến thức từ JSON thành văn bản thô
    context_text = f"THỦ TỤC: {data['thu_tuc']}\n\n"
    for intent in data['intents']:
        context_text += f"- Quy định: {intent['response']}\n"
        
    # 2. Xây dựng System Prompt (Giữ nguyên các quy tắc nghiêm ngặt của bạn)
    system_prompt = f"""Bạn là Trợ lý Ảo Hành chính công của Phường Sài Gòn.

[THÀNH PHẦN KIẾN THỨC CẤP PHÉP]
{context_text}

[QUY TẮC NGHIÊM NGẶT BẮT BUỘC TUÂN THỦ]
1. CHỈ ĐƯỢC PHÉP trả lời dựa trên nội dung trong [THÀNH PHẦN KIẾN THỨC CẤP PHÉP].
2. Tuyệt đối KHÔNG sáng tạo, KHÔNG lấy luật bên ngoài để trả lời.
3. Nếu câu hỏi hỏi về thủ tục khác (Kết hôn, Đất đai...) hoặc thông tin không có trong tài liệu trên, BẮT BUỘC trả lời: "Xin lỗi, hiện tại tôi chỉ được cung cấp dữ liệu về thủ tục {data['thu_tuc']}. Vui lòng liên hệ trực tiếp Bộ phận Một cửa để được hỗ trợ thủ tục này."
4. Cuối mỗi câu trả lời thành công, luôn khuyên người dân: "💡 Gợi ý: Bạn có thể nộp hồ sơ trực tuyến toàn trình tại [Cổng DVC Quốc Gia](https://dichvucong.gov.vn/) để tiết kiệm thời gian nhé."
5. Trình bày thân thiện, ngắn gọn, dùng Markdown."""

    # 3. Đóng gói Payload gửi lên API (Đúng chuẩn action: 'solve' của bạn)
    payload = {
        "action": "solve",
        "contents": [{"parts": [{"text": user_message}]}],
        "systemInstruction": {"parts": [{"text": system_prompt}]}
    }

    try:
        # Gửi request POST tới Google Apps Script
        response = requests.post(GOOGLE_APPS_SCRIPT_URL, json=payload)
        response_data = response.json()
        
        # Bóc tách kết quả trả về từ Gemini
        bot_text = response_data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
        
        if bot_text:
            return bot_text
        else:
            return "Hệ thống chưa nhận được phản hồi từ máy chủ ảo. Vui lòng thử lại."
            
    except Exception as e:
        return f"Hệ thống AI đang kết nối máy chủ. Vui lòng thử lại sau. (Lỗi: {str(e)})"