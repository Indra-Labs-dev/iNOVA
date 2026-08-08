import uuid

from app.repositories.conversation_repository import ConversationRepository


def test_create_conversation(db_session):
    repo = ConversationRepository(db_session)
    user_id = uuid.uuid4()

    conversation = repo.create(user_id=user_id)

    assert conversation.id is not None
    assert conversation.user_id == user_id


def test_get_for_user_returns_none_for_unknown_id(db_session):
    repo = ConversationRepository(db_session)
    assert repo.get_for_user(uuid.uuid4(), uuid.uuid4()) is None


def test_get_for_user_returns_none_when_owned_by_someone_else(db_session):
    repo = ConversationRepository(db_session)
    owner = uuid.uuid4()
    attacker = uuid.uuid4()
    conversation = repo.create(user_id=owner)

    assert repo.get_for_user(conversation.id, attacker) is None
    assert repo.get_for_user(conversation.id, owner) is not None


def test_list_for_user_scoped_and_ordered_most_recent_first(db_session):
    repo = ConversationRepository(db_session)
    user_a = uuid.uuid4()
    user_b = uuid.uuid4()

    first = repo.create(user_id=user_a)
    repo.create(user_id=user_b)
    second = repo.create(user_id=user_a)

    conversations = repo.list_for_user(user_a)

    assert [c.id for c in conversations] == [second.id, first.id]


def test_touch_bumps_updated_at_and_reorders_list(db_session):
    repo = ConversationRepository(db_session)
    user_id = uuid.uuid4()

    older = repo.create(user_id=user_id)
    newer = repo.create(user_id=user_id)

    repo.touch(older)

    conversations = repo.list_for_user(user_id)
    assert conversations[0].id == older.id
    assert conversations[1].id == newer.id


def test_delete_removes_the_conversation(db_session):
    repo = ConversationRepository(db_session)
    user_id = uuid.uuid4()
    conversation = repo.create(user_id=user_id)

    repo.delete(conversation)

    assert repo.get_for_user(conversation.id, user_id) is None
