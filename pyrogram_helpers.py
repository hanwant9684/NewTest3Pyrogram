# Pyrogram Helper Utilities
# Provides keyboard builders, message parsing, and utility functions for Pyrogram

from pyrogram.types import (
    InlineKeyboardButton as PyroButton,
    InlineKeyboardMarkup as PyroMarkup,
    Message
)
from typing import List, Optional, Tuple, Union
import re


def parse_command(text: str) -> List[str]:
    """
    Parse command and arguments from message text
    
    Args:
        text: Message text
        
    Returns:
        List of command parts (command is first element)
    """
    if not text or not text.startswith('/'):
        return []
    return text.split()


def get_command_args(text: str) -> List[str]:
    """Get command arguments only (without command itself)"""
    parts = parse_command(text)
    return parts[1:] if len(parts) > 1 else []


class InlineKeyboardButton:
    """Factory class to create Pyrogram inline keyboard buttons"""
    
    @staticmethod
    def callback(text: str, callback_data: str) -> PyroButton:
        """Create callback button"""
        return PyroButton(text=text, callback_data=callback_data)
    
    @staticmethod
    def url(text: str, url: str) -> PyroButton:
        """Create URL button"""
        return PyroButton(text=text, url=url)
    
    @staticmethod
    def switch_inline(text: str, switch_inline_query: str = "") -> PyroButton:
        """Create switch inline query button"""
        return PyroButton(text=text, switch_inline_query=switch_inline_query)


class InlineKeyboardMarkup:
    """Factory class to create Pyrogram inline keyboard markup"""
    
    def __init__(self, rows: List[List[PyroButton]]):
        """
        Create inline keyboard from rows of buttons
        
        Args:
            rows: List of button rows, each row is a list of buttons
        """
        self.rows = rows
        self._markup = PyroMarkup(rows)
    
    def to_pyrogram(self) -> PyroMarkup:
        """Convert to Pyrogram markup format"""
        return self._markup
    
    @property
    def inline_keyboard(self):
        """Get the inline keyboard rows"""
        return self.rows


def create_inline_keyboard(buttons: List[List[PyroButton]]) -> PyroMarkup:
    """
    Create inline keyboard from button layout
    
    Args:
        buttons: List of button rows
        
    Returns:
        Pyrogram InlineKeyboardMarkup
    """
    return PyroMarkup(buttons)


def get_message_link(chat_id: int, message_id: int, username: Optional[str] = None) -> str:
    """
    Generate Telegram message link
    
    Args:
        chat_id: Chat ID
        message_id: Message ID  
        username: Chat username (if public)
        
    Returns:
        Message link URL
    """
    if username:
        return f"https://t.me/{username}/{message_id}"
    else:
        chat_id_str = str(chat_id)
        if chat_id_str.startswith('-100'):
            chat_id_str = chat_id_str[4:]
        return f"https://t.me/c/{chat_id_str}/{message_id}"


def parse_message_link(link: str) -> Tuple[Optional[Union[str, int]], Optional[int], Optional[int]]:
    """
    Parse Telegram message link to extract chat and message IDs
    
    Args:
        link: Telegram message link
        
    Returns:
        Tuple of (chat_id_or_username, message_thread_id, message_id)
    """
    link = link.strip()
    
    if '?' in link:
        link = link.split('?')[0]
    
    parts = link.rstrip('/').split('/')
    
    try:
        if '/c/' in link:
            if len(parts) >= 7:
                channel_id = int(parts[-3])
                thread_id = int(parts[-2])
                message_id = int(parts[-1])
                return int(f"-100{channel_id}"), thread_id, message_id
            elif len(parts) >= 6:
                channel_id = int(parts[-2])
                message_id = int(parts[-1])
                return int(f"-100{channel_id}"), None, message_id
        else:
            if len(parts) >= 6:
                try:
                    username = parts[-3]
                    thread_id = int(parts[-2])
                    message_id = int(parts[-1])
                    return username, thread_id, message_id
                except ValueError:
                    pass
            
            if len(parts) >= 4:
                username = parts[-2]
                message_id = int(parts[-1])
                return username, None, message_id
    
    except (ValueError, IndexError):
        pass
    
    return None, None, None


def format_time(seconds: int) -> str:
    """
    Format seconds into readable time string
    
    Args:
        seconds: Time in seconds
        
    Returns:
        Formatted time string (e.g., "1h 23m 45s")
    """
    if seconds < 0:
        return "0s"
    
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if secs > 0 or not parts:
        parts.append(f"{secs}s")
    
    return " ".join(parts)


def format_size(bytes_size: int) -> str:
    """
    Format bytes into readable size string
    
    Args:
        bytes_size: Size in bytes
        
    Returns:
        Formatted size string (e.g., "1.23 GB")
    """
    if bytes_size < 0:
        return "0 B"
    
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    size = float(bytes_size)
    unit_index = 0
    
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    
    if unit_index == 0:
        return f"{int(size)} {units[unit_index]}"
    else:
        return f"{size:.2f} {units[unit_index]}"


async def get_display_name(user) -> str:
    """
    Get display name for a Pyrogram User object
    
    Args:
        user: Pyrogram User object
        
    Returns:
        Display name
    """
    if user is None:
        return "Unknown"
    
    if hasattr(user, 'first_name'):
        name = user.first_name or ""
        if hasattr(user, 'last_name') and user.last_name:
            name += f" {user.last_name}"
        return name.strip() or "Unknown"
    elif hasattr(user, 'title'):
        return user.title or "Unknown"
    return "Unknown"


def extract_code_from_message(text: str) -> Optional[str]:
    """
    Extract code/OTP from message text
    
    Args:
        text: Message text
        
    Returns:
        Extracted code or None
    """
    if not text:
        return None
    
    match = re.search(r'\b(\d{5,6})\b', text)
    if match:
        return match.group(1)
    
    return None


def get_sender_id(message: Message) -> Optional[int]:
    """
    Get sender ID from Pyrogram message (handles both user and channel messages)
    
    Args:
        message: Pyrogram Message object
        
    Returns:
        Sender ID or None
    """
    if message.from_user:
        return message.from_user.id
    elif message.sender_chat:
        return message.sender_chat.id
    return None


def get_chat_id(message: Message) -> int:
    """
    Get chat ID from Pyrogram message
    
    Args:
        message: Pyrogram Message object
        
    Returns:
        Chat ID
    """
    return message.chat.id


def get_message_text(message: Message) -> str:
    """
    Get text from Pyrogram message (handles text and caption)
    
    Args:
        message: Pyrogram Message object
        
    Returns:
        Message text or empty string
    """
    return message.text or message.caption or ""
