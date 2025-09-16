import bcrypt
import secrets
from database import DatabaseManager
from utils import validate_email, generate_unique_id

class AuthManager:
    """إدارة المصادقة والمستخدمين"""
    
    def __init__(self):
        self.db = DatabaseManager()
    
    def hash_password(self, password: str) -> str:
        """تشفير كلمة المرور"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """التحقق من كلمة المرور"""
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
        except:
            return False
    
    def register(self, username: str, email: str, password: str, display_name: str) -> bool:
        """تسجيل مستخدم جديد"""
        try:
            # التحقق من صحة البيانات
            if not all([username, email, password, display_name]):
                return False
            
            if not validate_email(email):
                return False
            
            if len(password) < 6:
                return False
            
            # تشفير كلمة المرور
            password_hash = self.hash_password(password)
            
            # إنشاء المستخدم
            user_id = self.db.create_user(username, email, password_hash, display_name)
            return user_id is not None
            
        except Exception as e:
            print(f"Error in register: {e}")
            return False
    
    def login(self, username: str, password: str) -> dict:
        """تسجيل الدخول"""
        try:
            # البحث عن المستخدم
            user = self.db.get_user_by_username(username)
            if not user:
                # محاولة البحث بالبريد الإلكتروني
                user = self.db.get_user_by_email(username)
            
            if user and self.verify_password(password, user['password_hash']):
                # تحديث حالة الاتصال
                self.db.update_user_online_status(user['id'], True)
                
                # إرجاع بيانات المستخدم بدون كلمة المرور
                return {
                    'id': user['id'],
                    'username': user['username'],
                    'email': user['email'],
                    'display_name': user['display_name'],
                    'avatar': user.get('avatar'),
                    'is_online': True
                }
            
            return None
            
        except Exception as e:
            print(f"Error in login: {e}")
            return None
    
    def logout(self, user_id: str) -> bool:
        """تسجيل الخروج"""
        try:
            self.db.update_user_online_status(user_id, False)
            return True
        except Exception as e:
            print(f"Error in logout: {e}")
            return False
    
    def change_password(self, user_id: str, old_password: str, new_password: str) -> bool:
        """تغيير كلمة المرور"""
        try:
            user = self.db.get_user_by_id(user_id)
            if not user:
                return False
            
            if not self.verify_password(old_password, user['password_hash']):
                return False
            
            if len(new_password) < 6:
                return False
            
            new_password_hash = self.hash_password(new_password)
            self.db.update_user_password(user_id, new_password_hash)
            return True
            
        except Exception as e:
            print(f"Error in change_password: {e}")
            return False
    
    def update_profile(self, user_id: str, display_name: str, email: str) -> bool:
        """تحديث الملف الشخصي"""
        try:
            if not validate_email(email):
                return False
            
            return self.db.update_user_profile(user_id, display_name, email)
            
        except Exception as e:
            print(f"Error in update_profile: {e}")
            return False
    
    def get_user_by_id(self, user_id: str) -> dict:
        """الحصول على بيانات المستخدم"""
        try:
            user = self.db.get_user_by_id(user_id)
            if user:
                # إزالة كلمة المرور من النتيجة
                user.pop('password_hash', None)
                return user
            return None
        except Exception as e:
            print(f"Error in get_user_by_id: {e}")
            return None
    
    def search_users(self, query: str, exclude_user_id: str) -> list:
        """البحث عن المستخدمين"""
        try:
            return self.db.search_users(query, exclude_user_id)
        except Exception as e:
            print(f"Error in search_users: {e}")
            return []
