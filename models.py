from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict, Any

@dataclass
class User:
    """نموذج المستخدم"""
    id: str
    username: str
    email: str
    display_name: str
    password_hash: Optional[str] = None
    avatar: Optional[str] = None
    is_online: bool = False
    last_seen: Optional[datetime] = None
    created_at: Optional[datetime] = None

@dataclass
class Friendship:
    """نموذج الصداقة"""
    id: str
    user_id: str
    friend_id: str
    status: str = "accepted"  # pending, accepted, blocked
    created_at: Optional[datetime] = None

@dataclass
class Conversation:
    """نموذج المحادثة"""
    id: str
    type: str = "private"  # private, group
    name: Optional[str] = None
    avatar: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@dataclass
class ConversationParticipant:
    """نموذج مشارك المحادثة"""
    id: str
    conversation_id: str
    user_id: str
    role: str = "member"  # member, admin
    joined_at: Optional[datetime] = None

@dataclass
class Message:
    """نموذج الرسالة"""
    id: str
    conversation_id: str
    sender_id: str
    content: str
    message_type: str = "text"  # text, file, image
    is_read: bool = False
    is_encrypted: bool = True  # تلقائياً مشفرة
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@dataclass
class EncryptionInfo:
    """معلومات التشفير"""
    method: str
    shift: int
    description: str
    security_level: str
    is_automatic: bool = True

@dataclass
class ChatStats:
    """إحصائيات الدردشة"""
    total_messages: int
    encrypted_messages: int
    total_conversations: int
    total_friends: int
    messages_today: int
    encryption_rate: float = 100.0  # 100% تلقائياً
    last_activity: Optional[datetime] = None

@dataclass
class UserStatus:
    """حالة المستخدم"""
    user_id: str
    is_online: bool
    last_seen: datetime
    current_conversation: Optional[str] = None
    encryption_active: bool = True

@dataclass
class SearchResult:
    """نتيجة البحث"""
    user_id: str
    username: str
    display_name: str
    email: str
    avatar: Optional[str] = None
    is_online: bool = False
    is_friend: bool = False

@dataclass
class ConversationDetails:
    """معلومات المحادثة المفصلة"""
    conversation: Conversation
    participants: List[User]
    last_message: Optional[Message] = None
    unread_count: int = 0
    is_encrypted: bool = True  # دائماً مشفرة

@dataclass
class MessageWithSender:
    """رسالة مع معلومات المرسل"""
    message: Message
    sender: User
    is_encrypted: bool = True
    decryption_status: str = "automatic"  # automatic, manual, failed

@dataclass
class EncryptionStatus:
    """حالة التشفير"""
    is_enabled: bool = True
    is_automatic: bool = True
    method: str = "Caesar Cipher"
    transparency_level: str = "complete"  # المستخدم لا يحتاج لمعرفة شيء
    user_intervention_required: bool = False

def create_user_from_dict(data: Dict[str, Any]) -> User:
    """إنشاء مستخدم من قاموس"""
    return User(
        id=data.get('id', ''),
        username=data.get('username', ''),
        email=data.get('email', ''),
        display_name=data.get('display_name', ''),
        password_hash=data.get('password_hash'),
        avatar=data.get('avatar'),
        is_online=data.get('is_online', False),
        last_seen=data.get('last_seen'),
        created_at=data.get('created_at')
    )

def create_message_from_dict(data: Dict[str, Any]) -> Message:
    """إنشاء رسالة من قاموس"""
    return Message(
        id=data.get('id', ''),
        conversation_id=data.get('conversation_id', ''),
        sender_id=data.get('sender_id', ''),
        content=data.get('content', ''),
        message_type=data.get('message_type', 'text'),
        is_read=data.get('is_read', False),
        is_encrypted=True,  # دائماً مشفرة
        created_at=data.get('created_at'),
        updated_at=data.get('updated_at')
    )

def create_conversation_from_dict(data: Dict[str, Any]) -> Conversation:
    """إنشاء محادثة من قاموس"""
    return Conversation(
        id=data.get('id', ''),
        type=data.get('type', 'private'),
        name=data.get('name'),
        avatar=data.get('avatar'),
        created_at=data.get('created_at'),
        updated_at=data.get('updated_at')
    )

def get_default_encryption_status() -> EncryptionStatus:
    """الحصول على حالة التشفير الافتراضية"""
    return EncryptionStatus(
        is_enabled=True,
        is_automatic=True,
        method="Caesar Cipher",
        transparency_level="complete",
        user_intervention_required=False
    )
