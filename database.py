import sqlite3
import secrets
from datetime import datetime
import json
import os

class DatabaseManager:
    """إدارة قاعدة البيانات"""
    
    def __init__(self, db_path="secure_chat.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """تهيئة قاعدة البيانات وإنشاء الجداول"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # جدول المستخدمين
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    display_name TEXT NOT NULL,
                    avatar TEXT,
                    is_online BOOLEAN DEFAULT FALSE,
                    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # جدول الصداقات
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS friendships (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    friend_id TEXT NOT NULL,
                    status TEXT DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id),
                    FOREIGN KEY (friend_id) REFERENCES users (id)
                )
            """)
            
            # جدول المحادثات
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversations (
                    id TEXT PRIMARY KEY,
                    type TEXT DEFAULT 'private',
                    name TEXT,
                    avatar TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # جدول مشاركي المحادثة
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS conversation_participants (
                    id TEXT PRIMARY KEY,
                    conversation_id TEXT NOT NULL,
                    user_id TEXT NOT NULL,
                    role TEXT DEFAULT 'member',
                    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (conversation_id) REFERENCES conversations (id),
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """)
            
            # جدول الرسائل
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id TEXT PRIMARY KEY,
                    conversation_id TEXT NOT NULL,
                    sender_id TEXT NOT NULL,
                    content TEXT NOT NULL,
                    message_type TEXT DEFAULT 'text',
                    is_read BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (conversation_id) REFERENCES conversations (id),
                    FOREIGN KEY (sender_id) REFERENCES users (id)
                )
            """)
            
            conn.commit()
    
    def generate_id(self):
        """توليد معرف فريد"""
        return secrets.token_hex(16)
    
    # إدارة المستخدمين
    def create_user(self, username, email, password_hash, display_name):
        """إنشاء مستخدم جديد"""
        user_id = self.generate_id()
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO users (id, username, email, password_hash, display_name)
                    VALUES (?, ?, ?, ?, ?)
                """, (user_id, username, email, password_hash, display_name))
                conn.commit()
                return user_id
        except sqlite3.IntegrityError:
            return None
    
    def get_user_by_username(self, username):
        """البحث عن مستخدم بواسطة اسم المستخدم"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, username, email, password_hash, display_name, avatar, 
                       is_online, last_seen, created_at
                FROM users WHERE username = ?
            """, (username,))
            row = cursor.fetchone()
            if row:
                return {
                    'id': row[0], 'username': row[1], 'email': row[2],
                    'password_hash': row[3], 'display_name': row[4], 'avatar': row[5],
                    'is_online': row[6], 'last_seen': row[7], 'created_at': row[8]
                }
            return None
    
    def get_user_by_email(self, email):
        """البحث عن مستخدم بواسطة البريد الإلكتروني"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, username, email, password_hash, display_name, avatar,
                       is_online, last_seen, created_at
                FROM users WHERE email = ?
            """, (email,))
            row = cursor.fetchone()
            if row:
                return {
                    'id': row[0], 'username': row[1], 'email': row[2],
                    'password_hash': row[3], 'display_name': row[4], 'avatar': row[5],
                    'is_online': row[6], 'last_seen': row[7], 'created_at': row[8]
                }
            return None
    
    def get_user_by_id(self, user_id):
        """البحث عن مستخدم بواسطة المعرف"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, username, email, password_hash, display_name, avatar,
                       is_online, last_seen, created_at
                FROM users WHERE id = ?
            """, (user_id,))
            row = cursor.fetchone()
            if row:
                return {
                    'id': row[0], 'username': row[1], 'email': row[2],
                    'password_hash': row[3], 'display_name': row[4], 'avatar': row[5],
                    'is_online': row[6], 'last_seen': row[7], 'created_at': row[8]
                }
            return None
    
    def update_user_online_status(self, user_id, is_online):
        """تحديث حالة الاتصال للمستخدم"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE users SET is_online = ?, last_seen = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (is_online, user_id))
            conn.commit()
    
    def search_users(self, query, exclude_user_id):
        """البحث عن المستخدمين"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, username, email, display_name, avatar, is_online, last_seen
                FROM users 
                WHERE (username LIKE ? OR email LIKE ? OR display_name LIKE ?)
                AND id != ?
                LIMIT 20
            """, (f"%{query}%", f"%{query}%", f"%{query}%", exclude_user_id))
            
            users = []
            for row in cursor.fetchall():
                users.append({
                    'id': row[0], 'username': row[1], 'email': row[2],
                    'display_name': row[3], 'avatar': row[4], 'is_online': row[5],
                    'last_seen': row[6]
                })
            return users
    
    def update_user_profile(self, user_id, display_name, email):
        """تحديث ملف المستخدم"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE users SET display_name = ?, email = ?
                    WHERE id = ?
                """, (display_name, email, user_id))
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False
    
    def update_user_password(self, user_id, new_password_hash):
        """تحديث كلمة مرور المستخدم"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE users SET password_hash = ?
                WHERE id = ?
            """, (new_password_hash, user_id))
            conn.commit()
    
    # إدارة الصداقات
    def create_friendship(self, user_id, friend_id):
        """إنشاء طلب صداقة"""
        friendship_id = self.generate_id()
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # التحقق من عدم وجود طلب صداقة موجود
                cursor.execute("""
                    SELECT id FROM friendships 
                    WHERE (user_id = ? AND friend_id = ?) OR (user_id = ? AND friend_id = ?)
                """, (user_id, friend_id, friend_id, user_id))
                
                if cursor.fetchone():
                    return None  # يوجد طلب صداقة بالفعل
                
                cursor.execute("""
                    INSERT INTO friendships (id, user_id, friend_id, status)
                    VALUES (?, ?, ?, 'accepted')
                """, (friendship_id, user_id, friend_id))
                conn.commit()
                return friendship_id
        except sqlite3.IntegrityError:
            return None
    
    def get_user_friends(self, user_id):
        """الحصول على قائمة أصدقاء المستخدم"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT u.id, u.username, u.display_name, u.avatar, u.is_online, u.last_seen
                FROM users u
                INNER JOIN friendships f ON (
                    (f.user_id = ? AND f.friend_id = u.id) OR
                    (f.friend_id = ? AND f.user_id = u.id)
                )
                WHERE f.status = 'accepted' AND u.id != ?
            """, (user_id, user_id, user_id))
            
            friends = []
            for row in cursor.fetchall():
                friends.append({
                    'id': row[0], 'username': row[1], 'display_name': row[2],
                    'avatar': row[3], 'is_online': row[4], 'last_seen': row[5]
                })
            return friends
    
    # إدارة المحادثات
    def create_conversation(self, conversation_type='private', name=None):
        """إنشاء محادثة جديدة"""
        conversation_id = self.generate_id()
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO conversations (id, type, name)
                    VALUES (?, ?, ?)
                """, (conversation_id, conversation_type, name))
                conn.commit()
                return conversation_id
        except Exception as e:
            print(f"Error creating conversation: {e}")
            return None
    
    def add_conversation_participant(self, conversation_id, user_id, role='member'):
        """إضافة مشارك للمحادثة"""
        participant_id = self.generate_id()
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO conversation_participants (id, conversation_id, user_id, role)
                    VALUES (?, ?, ?, ?)
                """, (participant_id, conversation_id, user_id, role))
                conn.commit()
                return participant_id
        except Exception as e:
            print(f"Error adding participant: {e}")
            return None
    
    def get_user_conversations(self, user_id):
        """الحصول على محادثات المستخدم"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT c.id, c.type, c.name, c.created_at,
                       (SELECT content FROM messages m WHERE m.conversation_id = c.id ORDER BY m.created_at DESC LIMIT 1) as last_message,
                       (SELECT u.display_name FROM users u 
                        INNER JOIN conversation_participants cp ON cp.user_id = u.id 
                        WHERE cp.conversation_id = c.id AND u.id != ? LIMIT 1) as other_user_name
                FROM conversations c
                INNER JOIN conversation_participants cp ON cp.conversation_id = c.id
                WHERE cp.user_id = ?
                ORDER BY c.updated_at DESC
            """, (user_id, user_id))
            
            conversations = []
            for row in cursor.fetchall():
                conv_name = row[2] if row[2] else row[5] if row[5] else "محادثة"
                conversations.append({
                    'id': row[0],
                    'type': row[1],
                    'name': conv_name,
                    'created_at': row[3],
                    'last_message': row[4] if row[4] else 'لا توجد رسائل'
                })
            return conversations
    
    def find_private_conversation(self, user1_id, user2_id):
        """البحث عن محادثة خاصة بين مستخدمين"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c.id, c.type, c.name, c.created_at
                FROM conversations c
                WHERE c.type = 'private'
                AND c.id IN (
                    SELECT cp1.conversation_id FROM conversation_participants cp1
                    WHERE cp1.user_id = ?
                )
                AND c.id IN (
                    SELECT cp2.conversation_id FROM conversation_participants cp2
                    WHERE cp2.user_id = ?
                )
            """, (user1_id, user2_id))
            
            row = cursor.fetchone()
            if row:
                # الحصول على اسم المستخدم الآخر
                other_user = self.get_user_by_id(user2_id)
                conv_name = other_user['display_name'] if other_user else "محادثة خاصة"
                
                return {
                    'id': row[0],
                    'type': row[1],
                    'name': conv_name,
                    'created_at': row[3]
                }
            return None
    
    # إدارة الرسائل
    def create_message(self, conversation_id, sender_id, content, message_type='text'):
        """إنشاء رسالة جديدة"""
        message_id = self.generate_id()
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO messages (id, conversation_id, sender_id, content, message_type)
                    VALUES (?, ?, ?, ?, ?)
                """, (message_id, conversation_id, sender_id, content, message_type))
                
                # تحديث وقت آخر نشاط للمحادثة
                cursor.execute("""
                    UPDATE conversations SET updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                """, (conversation_id,))
                
                conn.commit()
                return message_id
        except Exception as e:
            print(f"Error creating message: {e}")
            return None
    
    def get_conversation_messages(self, conversation_id, limit=50):
        """الحصول على رسائل المحادثة"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT m.id, m.conversation_id, m.sender_id, m.content, m.message_type,
                       m.created_at, u.username, u.display_name
                FROM messages m
                INNER JOIN users u ON u.id = m.sender_id
                WHERE m.conversation_id = ?
                ORDER BY m.created_at ASC
                LIMIT ?
            """, (conversation_id, limit))
            
            messages = []
            for row in cursor.fetchall():
                messages.append({
                    'id': row[0],
                    'conversation_id': row[1],
                    'sender_id': row[2],
                    'content': row[3],
                    'message_type': row[4],
                    'created_at': row[5],
                    'sender_username': row[6],
                    'sender_name': row[7]
                })
            return messages
