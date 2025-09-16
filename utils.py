import re
import html
import streamlit as st
from datetime import datetime
import os

def validate_input(text):
    """التحقق من صحة المدخلات"""
    if not text or not isinstance(text, str):
        return False
    
    # التحقق من الطول
    if len(text.strip()) == 0 or len(text) > 5000:
        return False
    
    # التحقق من المحتوى الضار
    dangerous_patterns = [
        r'<script.*?>.*?</script>',
        r'javascript:',
        r'data:text/html',
        r'<iframe.*?>.*?</iframe>',
        r'<object.*?>.*?</object>',
        r'<embed.*?>.*?</embed>'
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, text, re.IGNORECASE | re.DOTALL):
            return False
    
    return True

def sanitize_html(text):
    """تنظيف النص من HTML الضار"""
    if not text:
        return ""
    
    # تشفير HTML الخاص
    cleaned = html.escape(text)
    
    # إزالة الأسطر الفارغة الزائدة
    cleaned = re.sub(r'\n\s*\n', '\n\n', cleaned)
    
    # تحديد طول النص
    if len(cleaned) > 1000:
        cleaned = cleaned[:1000] + "..."
    
    return cleaned.strip()

def validate_email(email):
    """التحقق من صحة البريد الإلكتروني"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def generate_unique_id():
    """توليد معرف فريد"""
    import secrets
    return secrets.token_hex(16)

def format_timestamp(timestamp):
    """تنسيق الوقت للعرض"""
    if not timestamp:
        return ""
    
    try:
        if isinstance(timestamp, str):
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        else:
            dt = timestamp
        
        now = datetime.now()
        if hasattr(dt, 'replace'):
            dt = dt.replace(tzinfo=None)
        
        diff = now - dt
        
        if diff.days > 0:
            return f"منذ {diff.days} يوم"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"منذ {hours} ساعة"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"منذ {minutes} دقيقة"
        else:
            return "الآن"
    except:
        return "غير محدد"

def validate_username(username):
    """التحقق من صحة اسم المستخدم"""
    if not username or len(username) < 3 or len(username) > 20:
        return False
    
    # يجب أن يحتوي على أحرف وأرقام فقط
    pattern = r'^[a-zA-Z0-9_]+$'
    return re.match(pattern, username) is not None

def validate_display_name(name):
    """التحقق من صحة الاسم المعروض"""
    if not name or len(name.strip()) < 2 or len(name.strip()) > 50:
        return False
    
    # يجب ألا يحتوي على رموز خطيرة
    dangerous_chars = ['<', '>', '"', "'", '&', '\\', '/']
    return not any(char in name for char in dangerous_chars)

def clean_filename(filename):
    """تنظيف اسم الملف"""
    if not filename:
        return "file"
    
    # إزالة الأحرف الخطيرة
    cleaned = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # تحديد الطول
    if len(cleaned) > 100:
        name, ext = os.path.splitext(cleaned)
        cleaned = name[:100-len(ext)] + ext
    
    return cleaned or "file"

def format_file_size(size_bytes):
    """تنسيق حجم الملف"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

def get_file_icon(filename):
    """الحصول على أيقونة حسب نوع الملف"""
    if not filename:
        return "📄"
    
    ext = os.path.splitext(filename)[1].lower()
    
    icon_map = {
        '.pdf': '📄',
        '.doc': '📝', '.docx': '📝',
        '.txt': '📄',
        '.jpg': '🖼️', '.jpeg': '🖼️', '.png': '🖼️', '.gif': '🖼️',
        '.mp3': '🎵', '.wav': '🎵', '.m4a': '🎵',
        '.mp4': '🎬', '.avi': '🎬', '.mkv': '🎬',
        '.zip': '📦', '.rar': '📦', '.7z': '📦',
        '.py': '🐍', '.js': '💻', '.html': '🌐',
    }
    
    return icon_map.get(ext, '📄')

def truncate_text(text, max_length=100):
    """اقتطاع النص مع إضافة علامة القطع"""
    if not text or len(text) <= max_length:
        return text
    
    return text[:max_length-3] + "..."

def is_rtl_text(text):
    """التحقق من اتجاه النص (عربي أم لا)"""
    if not text:
        return False
    
    arabic_chars = sum(1 for char in text if '\u0600' <= char <= '\u06FF')
    total_chars = len([char for char in text if char.isalpha()])
    
    return arabic_chars > total_chars * 0.5 if total_chars > 0 else False

def escape_markdown(text):
    """تجنب رموز Markdown الخاصة"""
    if not text:
        return ""
    
    # رموز Markdown التي يجب تجنبها
    markdown_chars = ['*', '_', '`', '~', '>', '#', '+', '-', '=', '|', '{', '}', '[', ']', '(', ')', '!']
    
    for char in markdown_chars:
        text = text.replace(char, f'\\{char}')
    
    return text

def show_encryption_status():
    """عرض حالة التشفير للمستخدم"""
    st.info("🔐 **تم تفعيل التشفير التلقائي** - جميع رسائلك محمية تلقائياً!")

def show_security_badge():
    """عرض شارة الأمان"""
    return "🔐"

def get_system_status():
    """الحصول على حالة النظام"""
    return {
        "encryption_active": True,
        "automatic_mode": True,
        "user_intervention_required": False,
        "security_level": "متوسط",
        "method": "Caesar Cipher"
    }
