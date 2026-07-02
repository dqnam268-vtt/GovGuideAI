import streamlit as st
import time
from modules.bot_brain import get_response # Nạp bộ não AI vào giao diện

# 1. Cấu hình trang
st.set_page_config(page_title="GovGuide AI", page_icon="🤖", layout="centered")

st.title("🤖 GovGuide AI")
st.caption("Trợ lý Ảo Hỗ trợ Thủ tục Hành chính 24/7 - Phường Sài Gòn")
st.markdown("---")

# 2. Khởi tạo Bộ nhớ đệm (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant", 
            "content": "👋 Xin chào! Tôi là Trợ lý Ảo GovGuide của Phường Sài Gòn. Hiện tại tôi đã được nạp dữ liệu Thủ tục Đăng ký khai sinh. Bạn cần hỗ trợ thông tin gì ạ?"
        }
    ]

# 3. Hiển thị lịch sử trò chuyện
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Xử lý tin nhắn của người dùng
if prompt := st.chat_input("Ví dụ: Cần chuẩn bị giấy tờ gì để làm khai sinh?"):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("▌")
        time.sleep(0.6) # Giả lập độ trễ suy nghĩ của AI
        
        # --- ĐIỂM KẾT NỐI: Gọi Bot Brain để xử lý ---
        bot_response = get_response(prompt)
        # --------------------------------------------
        
        message_placeholder.markdown(bot_response)

    st.session_state.messages.append({"role": "assistant", "content": bot_response})