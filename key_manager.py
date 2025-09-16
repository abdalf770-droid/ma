import secrets
import os
from encryption_utils import CaesarCipher

class KeyManager:
    """إدارة مفاتيح التشفير التلقائي"""
    
    def __init__(self):
        """تهيئة مدير المفاتيح مع التشفير التلقائي"""
        self.caesar_shift = self._get_default_shift()
        self.cipher = CaesarCipher(self.caesar_shift)
    
    def _get_default_shift(self):
        """الحصول على الإزاحة الافتراضية من متغيرات البيئة أو قيمة افتراضية"""
        try:
            shift = int(os.getenv("ENCRYPTION_SHIFT", "7"))
            return shift if 1 <= shift <= 25 else 7
        except:
            return 7
    
    def get_caesar_shift(self):
        """الحصول على إزاحة قيصر الحالية"""
        return self.caesar_shift
    
    def set_caesar_shift(self, shift):
        """تحديد إزاحة قيصر جديدة"""
        if 1 <= shift <= 25:
            self.caesar_shift = shift
            self.cipher.set_shift(shift)
            return True
        return False
    
    def generate_random_shift(self):
        """توليد إزاحة عشوائية"""
        shift = secrets.randbelow(25) + 1
        self.set_caesar_shift(shift)
        return shift
    
    def encrypt(self, text):
        """تشفير النص تلقائياً - شفاف للمستخدم"""
        return self.cipher.encrypt(text)
    
    def decrypt(self, encrypted_text):
        """فك تشفير النص تلقائياً - شفاف للمستخدم"""
        return self.cipher.decrypt(encrypted_text)
    
    def get_encryption_info(self):
        """الحصول على معلومات التشفير"""
        return {
            "method": "Caesar Cipher",
            "shift": self.caesar_shift,
            "description": f"تشفير قيصر بإزاحة {self.caesar_shift}",
            "security_level": "متوسط" if self.caesar_shift != 13 else "منخفض (ROT13)",
            "is_automatic": True,
            "user_awareness": "شفاف - المستخدم لا يحتاج لمعرفة شيء"
        }
    
    def validate_key(self):
        """التحقق من صحة المفتاح"""
        return 1 <= self.caesar_shift <= 25
    
    def export_key(self):
        """تصدير المفتاح"""
        return {
            "caesar_shift": self.caesar_shift,
            "timestamp": secrets.token_hex(8),
            "method": "automatic_caesar"
        }
    
    def import_key(self, key_data):
        """استيراد المفتاح"""
        try:
            if "caesar_shift" in key_data:
                return self.set_caesar_shift(key_data["caesar_shift"])
            return False
        except:
            return False
    
    def rotate_key(self):
        """تدوير المفتاح (تغيير الإزاحة)"""
        old_shift = self.caesar_shift
        new_shift = self.generate_random_shift()
        
        return {
            "old_shift": old_shift,
            "new_shift": new_shift,
            "success": True,
            "message": "تم تدوير مفتاح التشفير تلقائياً"
        }
    
    def get_key_strength(self):
        """تقييم قوة المفتاح"""
        if self.caesar_shift == 13:
            return {
                "strength": "ضعيف",
                "score": 30,
                "reason": "استخدام ROT13 الشائع"
            }
        elif self.caesar_shift in [1, 25]:
            return {
                "strength": "ضعيف",
                "score": 40,
                "reason": "إزاحة ضعيفة جداً"
            }
        elif self.caesar_shift in [2, 3, 24, 23]:
            return {
                "strength": "متوسط",
                "score": 60,
                "reason": "إزاحة قابلة للتخمين"
            }
        else:
            return {
                "strength": "جيد",
                "score": 80,
                "reason": "إزاحة مناسبة للتشفير البسيط"
            }
    
    def generate_secure_shift(self):
        """توليد إزاحة آمنة نسبياً"""
        # تجنب الإزاحات الشائعة
        weak_shifts = [1, 2, 3, 13, 23, 24, 25]
        
        while True:
            shift = secrets.randbelow(25) + 1
            if shift not in weak_shifts:
                self.set_caesar_shift(shift)
                return shift
    
    def reset_to_default(self):
        """إعادة تعيين المفتاح للقيمة الافتراضية"""
        self.caesar_shift = self._get_default_shift()
        self.cipher.set_shift(self.caesar_shift)
    
    def get_all_keys(self):
        """الحصول على جميع المفاتيح (للتوافق مع الكود القديم)"""
        return {
            'caesar_shift': self.caesar_shift,
            'vigenere_key': None,
            'aes_key': None,
            'rsa_private_key': None,
            'rsa_public_key': None
        }
    
    def get_automatic_encryption_status(self):
        """الحصول على حالة التشفير التلقائي"""
        return {
            "is_active": True,
            "transparency": "تلقائي بالكامل",
            "user_interaction": "لا يحتاج المستخدم لفعل أي شيء",
            "encryption_on_send": True,
            "decryption_on_receive": True,
            "method": f"Caesar Cipher (Shift: {self.caesar_shift})"
        }
