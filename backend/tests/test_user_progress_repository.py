import uuid

import pytest

from app.repositories.user_progress_repository import UserProgressRepository


def test_get_returns_none_when_no_progress_yet(db_session):
    assert UserProgressRepository(db_session).get(uuid.uuid4()) is None


def test_add_xp_creates_progress_row_on_first_award(db_session):
    repo = UserProgressRepository(db_session)
    user_id = uuid.uuid4()

    progress = repo.add_xp(user_id, 10)

    assert progress.xp == 10
    assert repo.get(user_id).xp == 10


def test_add_xp_accumulates_across_calls(db_session):
    repo = UserProgressRepository(db_session)
    user_id = uuid.uuid4()

    repo.add_xp(user_id, 10)
    repo.add_xp(user_id, 10)
    progress = repo.add_xp(user_id, 5)

    assert progress.xp == 25


def test_add_xp_rejects_negative_amounts():
    # Security-relevant: there is no path to *decrease* XP through this
    # repository, and no path to set it to an arbitrary value either — only
    # ever additive, only ever server-driven.
    repo = UserProgressRepository(db=None)  # never reaches the DB — validated first
    with pytest.raises(ValueError):
        repo.add_xp(uuid.uuid4(), -100)


def test_progress_is_scoped_per_user(db_session):
    repo = UserProgressRepository(db_session)
    user_a = uuid.uuid4()
    user_b = uuid.uuid4()

    repo.add_xp(user_a, 50)

    assert repo.get(user_a).xp == 50
    assert repo.get(user_b) is None
