import streamlit as st
import bcrypt
import os
from datetime import datetime
from auth import AuthManager
from database import DatabaseManager
from encryption_utils import CaesarCipher
from chat_manager import ChatManager
from key_manager import KeyManager
from utils import validate_input, sanitize_html, format_timestamp

# تكوين الصفحة
st.set_page_config(
    page_title="SecureChat - الدردشة المشفرة",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تهيئة مديري النظام
@st.cache_resource
def init_managers():
    return {
        'auth': AuthManager(),
        'db': DatabaseManager(),
        'encryption': CaesarCipher(),
        'chat': ChatManager(),
        'key': KeyManager()
    }

managers = init_managers()

# تهيئة session state
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
if 'current_conversation' not in st.session_state:
    st.session_state.current_conversation = None
if 'page' not in st.session_state:
    st.session_state.page = 'login'

def show_header():
    """عرض رأس الصفحة مع معلومات المشروع"""
    st.markdown("""
    ### 🔐 SecureChat - الدردشة المشفرة
    **تصميم الطلاب:** عبدالفتاح الشيخ و ثابت العماد  
    **إشراف:** الدكتور صهيب
    ---
    """)

def show_login_page():
    """صفحة تسجيل الدخول"""
    show_header()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("## 🔐 تسجيل الدخول")
        st.markdown("مرحباً بك في تطبيق الدردشة المشفرة")
        
        with st.form("login_form"):
            username = st.text_input("👤 اسم المستخدم", placeholder="أدخل اسم المستخدم")
            password = st.text_input("🔒 كلمة المرور", type="password", placeholder="أدخل كلمة المرور")
            
            col_login, col_register = st.columns(2)
            
            with col_login:
                submit = st.form_submit_button("🚀 تسجيل الدخول", use_container_width=True, type="primary")
            
            with col_register:
                if st.form_submit_button("📝 إنشاء حساب جديد", use_container_width=True):
                    st.session_state.page = 'register'
                    st.rerun()
            
            if submit:
                if username and password:
                    user = managers['auth'].login(username, password)
                    if user:
                        st.session_state.current_user = user
                        st.session_state.page = 'chat'
                        st.success("✅ تم تسجيل الدخول بنجاح!")
                        st.rerun()
                    else:
                        st.error("❌ اسم المستخدم أو كلمة المرور غير صحيحة")
                else:
                    st.warning("⚠️ يرجى ملء جميع الحقول")

def show_register_page():
    """صفحة إنشاء حساب جديد"""
    show_header()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("## 📝 إنشاء حساب جديد")
        st.markdown("انضم إلى عالم الدردشة الآمنة")
        
        with st.form("register_form"):
            display_name = st.text_input("✨ الاسم الكامل", placeholder="أدخل اسمك الكامل")
            username = st.text_input("👤 اسم المستخدم", placeholder="اختر اسم مستخدم فريد")
            email = st.text_input("📧 البريد الإلكتروني", placeholder="أدخل بريدك الإلكتروني")
            password = st.text_input("🔒 كلمة المرور", type="password", placeholder="اختر كلمة مرور قوية")
            confirm_password = st.text_input("🔒 تأكيد كلمة المرور", type="password", placeholder="أعد كتابة كلمة المرور")
            
            col_register, col_back = st.columns(2)
            
            with col_register:
                submit = st.form_submit_button("🎉 إنشاء الحساب", use_container_width=True, type="primary")
            
            with col_back:
                if st.form_submit_button("← العودة لتسجيل الدخول", use_container_width=True):
                    st.session_state.page = 'login'
                    st.rerun()
            
            if submit:
                if all([display_name, username, email, password, confirm_password]):
                    if password != confirm_password:
                        st.error("❌ كلمتا المرور غير متطابقتين")
                    elif len(password) < 6:
                        st.error("❌ كلمة المرور يجب أن تكون 6 أحرف على الأقل")
                    else:
                        success = managers['auth'].register(username, email, password, display_name)
                        if success:
                            st.success("✅ تم إنشاء الحساب بنجاح! يمكنك الآن تسجيل الدخول")
                            st.session_state.page = 'login'
                            st.rerun()
                        else:
                            st.error("❌ فشل في إنشاء الحساب. اسم المستخدم أو البريد الإلكتروني مستخدم بالفعل")
                else:
                    st.warning("⚠️ يرجى ملء جميع الحقول")

def show_chat_interface():
    """واجهة الدردشة الرئيسية"""
    # شريط علوي مع معلومات المستخدم
    st.markdown(f"""
    ### 💬 SecureChat
    **مرحباً {st.session_state.current_user['display_name']}** 🟢 متصل  
    *تصميم: عبدالفتاح الشيخ و ثابت العماد | إشراف: د.صهيب*
    ---
    """)
    
    # الشريط الجانبي للمحادثات والأصدقاء
    with st.sidebar:
        st.markdown("### 📋 المحادثات والأصدقاء")
        
        # أزرار التنقل
        tab1, tab2 = st.tabs(["💬 المحادثات", "👥 الأصدقاء"])
        
        with tab1:
            show_conversations_tab()
        
        with tab2:
            show_friends_tab()
        
        # زر تسجيل الخروج
        st.markdown("---")
        if st.button("🚪 تسجيل الخروج", use_container_width=True):
            managers['db'].update_user_online_status(st.session_state.current_user['id'], False)
            st.session_state.current_user = None
            st.session_state.current_conversation = None
            st.session_state.page = 'login'
            st.rerun()
    
    # منطقة الدردشة الرئيسية
    if st.session_state.current_conversation:
        show_chat_area()
    else:
        show_welcome_screen()

def show_conversations_tab():
    """تبويب المحادثات"""
    conversations = managers['chat'].get_user_conversations(st.session_state.current_user['id'])
    
    if conversations:
        for conv in conversations:
            last_msg = conv.get('last_message', 'لا توجد رسائل')[:30] + "..." if len(conv.get('last_message', '')) > 30 else conv.get('last_message', 'لا توجد رسائل')
            
            if st.button(
                f"👤 **{conv['name']}**\n📝 {last_msg}",
                key=f"conv_{conv['id']}",
                use_container_width=True
            ):
                st.session_state.current_conversation = conv
                st.rerun()
    else:
        st.info("📭 لا توجد محادثات بعد")

def show_friends_tab():
    """تبويب الأصدقاء"""
    search_query = st.text_input("🔍 البحث عن أصدقاء", key="friend_search")
    
    friends = managers['chat'].get_user_friends(st.session_state.current_user['id'])
    
    if friends:
        for friend in friends:
            col1, col2 = st.columns([3, 1])
            with col1:
                status = "🟢" if friend.get('is_online') else "⚫"
                st.write(f"{status} **{friend['display_name']}**")
            with col2:
                if st.button("💬", key=f"chat_{friend['id']}", help="بدء محادثة"):
                    conv = managers['chat'].get_or_create_conversation(
                        st.session_state.current_user['id'], 
                        friend['id']
                    )
                    if conv:
                        st.session_state.current_conversation = conv
                        st.rerun()
    else:
        st.info("👥 لا توجد أصدقاء بعد")
    
    # إضافة صديق جديد
    st.markdown("---")
    with st.expander("➕ إضافة صديق جديد"):
        search_query = st.text_input("البحث بالاسم أو البريد الإلكتروني")
        if search_query and len(search_query) > 2:
            users = managers['db'].search_users(search_query, st.session_state.current_user['id'])
            for user in users:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"👤 **{user['display_name']}** (@{user['username']})")
                with col2:
                    if st.button("➕", key=f"add_{user['id']}", help="إرسال طلب صداقة"):
                        success = managers['chat'].send_friend_request(
                            st.session_state.current_user['id'], 
                            user['id']
                        )
                        if success:
                            st.success("✅ تم إرسال طلب الصداقة!")
                            st.rerun()
                        else:
                            st.error("❌ فشل في إرسال طلب الصداقة")

def show_chat_area():
    """منطقة الدردشة"""
    conv = st.session_state.current_conversation
    
    # رأس المحادثة
    st.markdown(f"""
    ### 💬 {conv['name']}
    *محادثة خاصة مشفرة تلقائياً* 🔐
    ---
    """)
    
    # منطقة الرسائل
    messages_container = st.container()
    
    with messages_container:
        messages = managers['chat'].get_conversation_messages(conv['id'])
        
        if messages:
            for msg in messages[-50:]:  # آخر 50 رسالة
                is_sent = msg['sender_id'] == st.session_state.current_user['id']
                
                # فك التشفير التلقائي
                decrypted_content = managers['encryption'].decrypt(msg['content'])
                
                # تصميم الرسالة
                timestamp = format_timestamp(msg.get('created_at', ''))
                sender_name = "أنت" if is_sent else msg.get('sender_name', 'مستخدم')
                
                if is_sent:
                    st.markdown(f"""
                    <div style='text-align: right; margin: 10px 0;'>
                        <div style='background-color: #dcf8c6; padding: 10px 15px; border-radius: 15px; display: inline-block; max-width: 70%; border: 1px solid #a5d6a7;'>
                            <strong>{sender_name}:</strong><br>
                            {sanitize_html(decrypted_content)}<br>
                            <small style='color: #666;'>{timestamp} 🔐</small>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style='text-align: left; margin: 10px 0;'>
                        <div style='background-color: #ffffff; padding: 10px 15px; border-radius: 15px; display: inline-block; max-width: 70%; border: 1px solid #ddd;'>
                            <strong>{sender_name}:</strong><br>
                            {sanitize_html(decrypted_content)}<br>
                            <small style='color: #666;'>{timestamp} 🔐</small>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("🎉 ابدأ المحادثة بإرسال أول رسالة!")
    
    # منطقة إرسال الرسائل
    st.markdown("---")
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        message_input = st.text_area(
            "✍️ اكتب رسالتك هنا...",
            height=100,
            key="message_input",
            placeholder="اكتب رسالة واضغط إرسال للتشفير التلقائي..."
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📤 إرسال", use_container_width=True, type="primary"):
            if message_input and message_input.strip():
                if validate_input(message_input):
                    # التشفير التلقائي
                    encrypted_content = managers['encryption'].encrypt(message_input.strip())
                    
                    # إرسال الرسالة المشفرة
                    success = managers['chat'].send_message(
                        st.session_state.current_user['id'],
                        conv['id'],
                        encrypted_content
                    )
                    
                    if success:
                        st.success("✅ تم إرسال الرسالة المشفرة!")
                        # مسح النص
                        st.session_state.message_input = ""
                        st.rerun()
                    else:
                        st.error("❌ فشل في إرسال الرسالة")
                else:
                    st.error("❌ الرسالة تحتوي على محتوى غير مسموح")
            else:
                st.warning("⚠️ لا يمكن إرسال رسالة فارغة")

def show_welcome_screen():
    """شاشة الترحيب"""
    st.markdown("""
    ## 🎉 مرحباً بك في SecureChat
    
    ### تطبيق الدردشة المشفرة الآمن
    
    #### ✨ الميزات:
    
    - 🔐 **تشفير تلقائي**: جميع رسائلك محمية بتشفير قيصر المتطور
    - ⚡ **سريع وآمن**: إرسال فوري مع أقصى درجات الحماية  
    - 👥 **إدارة الأصدقاء**: أضف أصدقاءك وابدأ المحادثات بسهولة
    - 🔒 **حماية البيانات**: قاعدة بيانات مشفرة وآمنة
    
    ---
    
    👈 **للبدء:** اختر محادثة من الشريط الجانبي أو أضف صديق جديد
    
    ---
    
    *التشفير يتم تلقائياً - لا تحتاج لفعل أي شيء إضافي!*
    """)

# تحديث حالة الاتصال
if st.session_state.current_user:
    managers['db'].update_user_online_status(st.session_state.current_user['id'], True)

# التنقل بين الصفحات
if st.session_state.page == 'login':
    show_login_page()
elif st.session_state.page == 'register':
    show_register_page()
elif st.session_state.page == 'chat' and st.session_state.current_user:
    show_chat_interface()
else:
    st.session_state.page = 'login'
    st.rerun()
