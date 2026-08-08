import uuid

from app.models.message import MessageRole
from app.repositories.conversation_repository import ConversationRepository
from app.repositories.message_repository import MessageRepository


def _conversation(db_session):
    return ConversationRepository(db_session).create(user_id=uuid.uuid4())


def test_add_message(db_session):
    conversation = _conversation(db_session)
    repo = MessageRepository(db_session)

    message = repo.add(conversation_id=conversation.id, role=MessageRole.USER.value, content="hello")

    assert message.id is not None
    assert message.role == "user"
    assert message.content == "hello"


def test_list_for_conversation_returns_oldest_first(db_session):
    conversation = _conversation(db_session)
    repo = MessageRepository(db_session)
    repo.add(conversation_id=conversation.id, role=MessageRole.USER.value, content="first")
    repo.add(conversation_id=conversation.id, role=MessageRole.ASSISTANT.value, content="second")
    repo.add(conversation_id=conversation.id, role=MessageRole.USER.value, content="third")

    messages = repo.list_for_conversation(conversation.id)

    assert [m.content for m in messages] == ["first", "second", "third"]


def test_list_for_conversation_scoped_to_conversation(db_session):
    conv_a = _conversation(db_session)
    conv_b = _conversation(db_session)
    repo = MessageRepository(db_session)
    repo.add(conversation_id=conv_a.id, role=MessageRole.USER.value, content="in A")
    repo.add(conversation_id=conv_b.id, role=MessageRole.USER.value, content="in B")

    messages = repo.list_for_conversation(conv_a.id)

    assert [m.content for m in messages] == ["in A"]


def test_recent_for_conversation_bounds_and_preserves_chronological_order(db_session):
    conversation = _conversation(db_session)
    repo = MessageRepository(db_session)
    for i in range(5):
        repo.add(conversation_id=conversation.id, role=MessageRole.USER.value, content=f"msg-{i}")

    recent = repo.recent_for_conversation(conversation.id, limit=3)

    assert [m.content for m in recent] == ["msg-2", "msg-3", "msg-4"]


def test_recent_for_conversation_returns_all_when_fewer_than_limit(db_session):
    conversation = _conversation(db_session)
    repo = MessageRepository(db_session)
    repo.add(conversation_id=conversation.id, role=MessageRole.USER.value, content="only one")

    recent = repo.recent_for_conversation(conversation.id, limit=10)

    assert [m.content for m in recent] == ["only one"]
