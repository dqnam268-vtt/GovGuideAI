import json
import os

def load_knowledge():
    """Hàm nạp thành phần kiến thức từ các file JSON."""
    knowledge_path = os.path.join(os.path.dirname(__file__), '..', 'knowledge_base', '01_khai_sinh.json')
    try:
        with open(knowledge_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        return None

def get_response(user_message):
    """Hàm xử lý logic và trả về kết quả."""
    data = load_knowledge()
    
    if not data:
        return "Xin lỗi, hệ thống dữ liệu đang được bảo trì. Vui lòng thử lại sau."

    # Tiền xử lý câu hỏi: chuyển về chữ thường để dễ so sánh
    message_lower = user_message.lower()
    
    # Kiểm tra xem người dùng có đang hỏi về Khai sinh không
    if "khai sinh" in message_lower or "đẻ" in message_lower or "em bé" in message_lower:
        
        # Duyệt qua các kịch bản (intents) trong thành phần kiến thức
        for intent in data['intents']:
            for keyword in intent['keywords']:
                if keyword in message_lower:
                    # Tích hợp Call-to-action thúc đẩy trực tuyến vào mọi câu trả lời
                    base_response = intent['response']
                    if "trực tuyến" not in keyword: # Tránh lặp lại câu mời nộp online nếu họ đã hỏi về online
                        base_response += "\n\n💡 **Gợi ý:** Để tiết kiệm thời gian, bạn có thể [Nộp hồ sơ trực tuyến tại đây](#)."
                    return base_response
        
        # Nếu hỏi về khai sinh nhưng không rõ ý (ví dụ: "cho tôi hỏi về khai sinh")
        return data['default_response']
    
    # Nếu hỏi ngoài lề
    return "Hiện tại tôi là Trợ lý ảo chuyên hỗ trợ thủ tục **Đăng ký Khai sinh**. Các thủ tục khác như Kết hôn, Đất đai đang được cập nhật. Bạn cần hỗ trợ gì về Khai sinh ạ?"