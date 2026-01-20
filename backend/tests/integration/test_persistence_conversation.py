import pytest
import uuid
from api.database.session import get_db_session
from api.database.repositories.conversation_repository import ConversationRepository
from api.database.models.message import MessageRole

@pytest.mark.asyncio
async def test_conversation_flow():
    async for session in get_db_session():
        repo = ConversationRepository(session)
        user_id = str(uuid.uuid4())
        
        conv = await repo.create_conversation(user_id)
        msg1 = await repo.add_message(conv.id, MessageRole.USER, "Hi")
        msg2 = await repo.add_message(conv.id, MessageRole.ASSISTANT, "Hello")
        
        history = await repo.get_history(conv.id)
        assert len(history) == 2
        assert history[0].content == "Hi"
        assert history[1].content == "Hello"
        
        # Cleanup
        await session.delete(msg1)
        await session.delete(msg2)
        await session.delete(conv)
        await session.commit()
        return
