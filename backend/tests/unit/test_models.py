import pytest
from uuid import uuid4
from api.database.models.task import Task, TaskStatus
from api.database.models.conversation import Conversation
from api.database.models.message import Message, MessageRole
from api.database.models.user import User

def test_task_model_validation():
    user_id = str(uuid4())
    task = Task(title="Buy milk", user_id=user_id)
    assert task.title == "Buy milk"
    assert task.status == TaskStatus.PENDING
    assert task.created_at is not None
    assert task.user_id == user_id

def test_conversation_model():
    user_id = str(uuid4())
    conv = Conversation(user_id=user_id)
    assert conv.user_id == user_id
    assert conv.title is None

def test_message_model():
    conv_id = uuid4()
    msg = Message(conversation_id=conv_id, role=MessageRole.USER, content="Hello")
    assert msg.role == MessageRole.USER
    assert msg.content == "Hello"

def test_user_model():
    user = User(name="Test", email="test@test.com")
    assert user.is_active is True
