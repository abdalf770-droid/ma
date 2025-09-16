import streamlit as st
import uuid
import datetime
from encryption import encrypt_message, decrypt_message

# محاكاة قاعدة بيانات في الذاكرة (ممكن تربطها بـ PostgreSQL لاحقاً)
MESSAGES = []
USERS = {"1": "خالد", "2": "أحمد"}  # مستخدمين تجريبيين

def save_message(conversation_id, sender_id, content):
    """حفظ رسالة في قاعدة البيانات (مشفرة)"""
    encrypted_content = encrypt_message(content)
    MESSAGES.append({
        "id": str(uuid.uuid4()),
        "conversation_id": conversation_id,
        "sender_id": sender_id,
        "content": encrypted_content,  # نخزن النص مشفر
        "created_at": datetime.datetime.now()
    })

def get_messages(conversation_id):
    """جلب الرسائل مع فك التشفير"""
    msgs = [m for m in MESSAGES if m["conversation_id"] == conversation_id]
    for m in msgs:
        m["decrypted"] = decrypt_message(m["content"])
    return msgs

def show_chat_interface():
    st.title("💬 SecureChat - محادثة مشفرة")

    # تحديد المستخدم الحالي
    current_user = st.selectbox("اختر المستخدم", list(USERS.keys()), format_func=lambda x: USERS[x])
    conversation_id = "conv1"  # محادثة واحدة تجريبية

    # عرض الرسائل
    st.subheader("📥 الرسائل")
    messages = get_messages(conversation_id)
    for m in messages:
        sender = USERS[m["sender_id"]]
        st.markdown(f"**{sender}**: {m['decrypted']}  \n<sub>📅 {m['created_at'].strftime('%Y-%m-%d %H:%M:%S')}</sub>")

    # كتابة رسالة جديدة
    st.subheader("✍️ أرسل رسالة")
    msg = st.text_input("اكتب رسالتك هنا", key="message_input")

    if st.button("إرسال"):
        if msg.strip():
            save_message(conversation_id, current_user, msg)
            st.session_state.message_input = ""  # تنظيف الحقل بعد الإرسال
            st.rerun()  # تحديث واجهة المحادثة

def main():
    show_chat_interface()

if __name__ == "__main__":
    main()
