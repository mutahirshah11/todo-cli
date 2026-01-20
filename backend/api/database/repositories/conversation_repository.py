from uuid import UUID
from typing import List, Optional
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from api.database.models.conversation import Conversation
from api.database.models.message import Message, MessageRole

class ConversationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_conversation(self, user_id: str, title: Optional[str] = None) -> Conversation:
        conversation = Conversation(user_id=user_id, title=title)
        self.session.add(conversation)
        await self.session.commit()
        await self.session.refresh(conversation)
        return conversation

    async def add_message(self, conversation_id: UUID, role: MessageRole, content: str) -> Message:
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content
        )
        self.session.add(message)
        await self.session.commit()
        await self.session.refresh(message)
        return message

    async def get_history(self, conversation_id: UUID, limit: int = 50) -> List[Message]:
        statement = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.asc()).limit(limit)
        
        result = await self.session.execute(statement)
        return result.scalars().all()
