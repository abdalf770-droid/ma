import secrets
import string

class CaesarCipher:
    """تشفير قيصر المبسط للرسائل مع التشفير التلقائي"""
    
    def __init__(self, default_shift=7):
        """تهيئة المشفر مع إزاحة افتراضية"""
        self.default_shift = default_shift
    
    def encrypt(self, text, shift=None):
        """تشفير النص باستخدام تشفير قيصر التلقائي"""
        if shift is None:
            shift = self.default_shift
            
        result = ""
        for char in text:
            if char.isalpha():
                # تحديد الأساس (A أو a)
                ascii_offset = 65 if char.isupper() else 97
                # تطبيق الإزاحة مع التدوير
                shifted = (ord(char) - ascii_offset + shift) % 26
                result += chr(shifted + ascii_offset)
            elif char.isdigit():
                # تشفير الأرقام
                shifted = (int(char) + shift) % 10
                result += str(shifted)
            else:
                # الاحتفاظ بالرموز كما هي
                result += char
        
        return result
    
    def decrypt(self, encrypted_text, shift=None):
        """فك تشفير النص تلقائياً"""
        if shift is None:
            shift = self.default_shift
            
        result = ""
        for char in encrypted_text:
            if char.isalpha():
                # تحديد الأساس (A أو a)
                ascii_offset = 65 if char.isupper() else 97
                # عكس الإزاحة مع التدوير
                shifted = (ord(char) - ascii_offset - shift) % 26
                result += chr(shifted + ascii_offset)
            elif char.isdigit():
                # فك تشفير الأرقام
                shifted = (int(char) - shift) % 10
                result += str(shifted)
            else:
                # الاحتفاظ بالرموز كما هي
                result += char
        
        return result
    
    def generate_random_shift(self):
        """توليد إزاحة عشوائية"""
        return secrets.randbelow(25) + 1
    
    def set_shift(self, shift):
        """تحديد إزاحة جديدة"""
        if 1 <= shift <= 25:
            self.default_shift = shift
            return True
        return False
    
    def get_shift(self):
        """الحصول على الإزاحة الحالية"""
        return self.default_shift
    
    def encrypt_with_key(self, text, key_phrase):
        """تشفير باستخدام عبارة مفتاح"""
        # تحويل العبارة إلى رقم
        key_sum = sum(ord(c) for c in key_phrase if c.isalnum())
        shift = (key_sum % 25) + 1
        return self.encrypt(text, shift)
    
    def decrypt_with_key(self, encrypted_text, key_phrase):
        """فك التشفير باستخدام عبارة مفتاح"""
        # تحويل العبارة إلى رقم
        key_sum = sum(ord(c) for c in key_phrase if c.isalnum())
        shift = (key_sum % 25) + 1
        return self.decrypt(encrypted_text, shift)
    
    def get_encryption_info(self):
        """الحصول على معلومات التشفير"""
        return {
            "method": "Caesar Cipher",
            "shift": self.default_shift,
            "description": f"تشفير قيصر بإزاحة {self.default_shift}",
            "security_level": "متوسط" if self.default_shift != 13 else "منخفض (ROT13)",
            "is_automatic": True
        }


class AdvancedCaesarCipher(CaesarCipher):
    """تشفير قيصر متطور مع تحسينات إضافية"""
    
    def __init__(self):
        super().__init__(default_shift=13)  # ROT13 كافتراضي
        self.custom_alphabet = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    def advanced_encrypt(self, text):
        """تشفير متطور مع خلط الأحرف"""
        # المرحلة الأولى: تشفير قيصر عادي
        stage1 = self.encrypt(text)
        
        # المرحلة الثانية: عكس النص
        stage2 = stage1[::-1]
        
        # المرحلة الثالثة: تبديل الأحرف بطريقة معينة
        result = ""
        for i, char in enumerate(stage2):
            if char.isalpha():
                if i % 2 == 0:
                    result += char.upper() if char.islower() else char.lower()
                else:
                    result += char
            else:
                result += char
        
        return result
    
    def advanced_decrypt(self, encrypted_text):
        """فك التشفير المتطور"""
        # عكس المرحلة الثالثة: إرجاع تبديل الأحرف
        stage1 = ""
        for i, char in enumerate(encrypted_text):
            if char.isalpha():
                if i % 2 == 0:
                    stage1 += char.upper() if char.islower() else char.lower()
                else:
                    stage1 += char
            else:
                stage1 += char
        
        # عكس المرحلة الثانية: عكس النص
        stage2 = stage1[::-1]
        
        # عكس المرحلة الأولى: فك تشفير قيصر
        result = self.decrypt(stage2)
        
        return result


class MessageEncryptor:
    """مشفر الرسائل الرئيسي للتطبيق - تلقائي وشفاف"""
    
    def __init__(self):
        self.caesar = CaesarCipher(default_shift=7)
        self.advanced = AdvancedCaesarCipher()
        self.encryption_method = "simple"  # simple أو advanced
    
    def encrypt_message(self, message):
        """تشفير الرسالة تلقائياً حسب الطريقة المحددة"""
        if self.encryption_method == "advanced":
            return self.advanced.advanced_encrypt(message)
        else:
            return self.caesar.encrypt(message)
    
    def decrypt_message(self, encrypted_message):
        """فك تشفير الرسالة تلقائياً حسب الطريقة المحددة"""
        if self.encryption_method == "advanced":
            return self.advanced.advanced_decrypt(encrypted_message)
        else:
            return self.caesar.decrypt(encrypted_message)
    
    def set_encryption_method(self, method):
        """تحديد طريقة التشفير"""
        if method in ["simple", "advanced"]:
            self.encryption_method = method
            return True
        return False
    
    def get_encryption_info(self):
        """الحصول على معلومات التشفير"""
        return {
            "method": self.encryption_method,
            "shift": self.caesar.get_shift(),
            "description": "تشفير قيصر متطور" if self.encryption_method == "advanced" else "تشفير قيصر بسيط",
            "is_automatic": True,
            "transparency": "المستخدم لا يحتاج لفعل أي شيء - التشفير تلقائي"
        }


# المشفر الافتراضي للتطبيق
DEFAULT_ENCRYPTOR = MessageEncryptor()

def encrypt_text(text):
    """دالة مساعدة لتشفير النص تلقائياً"""
    return DEFAULT_ENCRYPTOR.encrypt_message(text)

def decrypt_text(encrypted_text):
    """دالة مساعدة لفك التشفير تلقائياً"""
    return DEFAULT_ENCRYPTOR.decrypt_message(encrypted_text)

def get_encryption_status():
    """الحصول على حالة التشفير"""
    return DEFAULT_ENCRYPTOR.get_encryption_info()
