from datetime import datetime
from typing import List, Dict, Optional
from database import DatabaseManager
from encryption_utils import CaesarCipher
from utils import validate_input, sanitize_html

class ChatManager:
    """إدارة الدردشة والرسائل المشفرة تلقائياً"""
    
    def __init__(self):
        self.db = DatabaseManager()
        self.encryptor = CaesarCipher()
    
    def get_user_conversations(self, user_id: str) -> List[Dict]:
        """الحصول على محادثات المستخدم"""
        try:
            return self.db.get_user_conversations(user_id)
        except Exception as e:
            print(f"Error getting conversations: {e}")
            return []
    
    def get_conversation_messages(self, conversation_id: str, limit: int = 50) -> List[Dict]:
        """الحصول على رسائل المحادثة"""
        try:
            return self.db.get_conversation_messages(conversation_id, limit)
        except Exception as e:
            print(f"Error getting messages: {e}")
            return []
    
    def send_message(self, sender_id: str, conversation_id: str, encrypted_content: str) -> bool:
        """إرسال رسالة مشفرة (المحتوى مشفر بالفعل)"""
        try:
            # التحقق من صحة المحتوى المشفر
            if not encrypted_content or not encrypted_content.strip():
                return False
            
            # حفظ الرسالة المشفرة في قاعدة البيانات
            message_id = self.db.create_message(
                conversation_id=conversation_id,
                sender_id=sender_id,
                content=encrypted_content,  # المحتوى مشفر بالفعل
                message_type='text'
            )
            
            return message_id is not None
            
        except Exception as e:
            print(f"Error sending message: {e}")
            return False
    
    def create_conversation(self, user1_id: str, user2_id: str) -> Optional[Dict]:
        """إنشاء محادثة جديدة بين مستخدمين"""
        try:
            # التحقق من وجود محادثة مسبقة
            existing_conversation = self.db.find_private_conversation(user1_id, user2_id)
            if existing_conversation:
                return existing_conversation
            
            # إنشاء محادثة جديدة
            conversation_id = self.db.create_conversation('private')
            
            if not conversation_id:
                return None
            
            # إضافة المشاركين
            self.db.add_conversation_participant(conversation_id, user1_id, 'admin')
            self.db.add_conversation_participant(conversation_id, user2_id, 'member')
            
            # الحصول على اسم المحادثة (اسم المستخدم الآخر)
            other_user = self.db.get_user_by_id(user2_id)
            conversation_name = other_user['display_name'] if other_user else "محادثة خاصة"
            
            return {
                'id': conversation_id,
                'type': 'private',
                'name': conversation_name,
                'created_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error creating conversation: {e}")
            return None
    
    def get_or_create_conversation(self, user1_id: str, user2_id: str) -> Optional[Dict]:
        """الحصول على محادثة أو إنشاؤها إذا لم تكن موجودة"""
        try:
            # البحث عن محادثة موجودة
            existing_conversation = self.db.find_private_conversation(user1_id, user2_id)
            if existing_conversation:
                return existing_conversation
            
            # إنشاء محادثة جديدة
            return self.create_conversation(user1_id, user2_id)
            
        except Exception as e:
            print(f"Error getting or creating conversation: {e}")
            return None
    
    def get_user_friends(self, user_id: str) -> List[Dict]:
        """الحصول على قائمة أصدقاء المستخدم"""
        try:
            return self.db.get_user_friends(user_id)
        except Exception as e:
            print(f"Error getting friends: {e}")
            return []
    
    def send_friend_request(self, sender_id: str, receiver_id: str) -> bool:
        """إرسال طلب صداقة"""
        try:
            # التحقق من عدم إرسال الطلب لنفس المستخدم
            if sender_id == receiver_id:
                return False
            
            # التحقق من وجود المستخدم المستقبل
            receiver = self.db.get_user_by_id(receiver_id)
            if not receiver:
                return False
            
            # إنشاء طلب الصداقة (مقبول تلقائياً للبساطة)
            friendship_id = self.db.create_friendship(sender_id, receiver_id)
            return friendship_id is not None
            
        except Exception as e:
            print(f"Error sending friend request: {e}")
            return False
    
    def search_users(self, query: str, exclude_user_id: str) -> List[Dict]:
        """البحث عن المستخدمين"""
        try:
            return self.db.search_users(query, exclude_user_id)
        except Exception as e:
            print(f"Error searching users: {e}")
            return []
    
    def mark_conversation_as_read(self, conversation_id: str, user_id: str) -> bool:
        """تمييز المحادثة كمقروءة"""
        try:
            # يمكن تطوير هذه الوظيفة لاحقاً
            return True
        except Exception as e:
            print(f"Error marking as read: {e}")
            return False
    
    def get_unread_count(self, user_id: str) -> int:
        """الحصول على عدد الرسائل غير المقروءة"""
        try:
            # يمكن تطوير هذه الوظيفة لاحقاً
            return 0
        except Exception as e:
            print(f"Error getting unread count: {e}")
            return 0
    
    def delete_message(self, message_id: str, user_id: str) -> bool:
        """حذف رسالة"""
        try:
            # يمكن تطوير هذه الوظيفة لاحقاً
            return True
        except Exception as e:
            print(f"Error deleting message: {e}")
            return False
    
    def get_conversation_info(self, conversation_id: str) -> Optional[Dict]:
        """الحصول على معلومات المحادثة"""
        try:
            # يمكن تطوير هذه الوظيفة لاحقاً
            return None
        except Exception as e:
            print(f"Error getting conversation info: {e}")
            return None
    
    def get_encryption_status(self) -> Dict:
        """الحصول على حالة التشفير"""
        return self.encryptor.get_encryption_info()
