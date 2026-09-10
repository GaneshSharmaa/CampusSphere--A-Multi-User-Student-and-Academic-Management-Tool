from users.models import User
from membership.models import Membership
from institutes.models import Institute

async def test_create_user(db_session):
    user = User(
        email="test@example.com",
        phone="9876543210",
        hashed_password="hashed-password",
    )

    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    assert user.id is not None
    assert user.email == "test@example.com"

async def test_user_membership_relationship(
    db_session,
):
    user = User(
        email="test@example.com",
        phone="9876543210",
        hashed_password="hashed",
    )

    institute = Institute(
        institute_code="ABC123",
        institute_name="Test Institute",
    )

    db_session.add_all([user, institute])
    await db_session.commit()

    membership = Membership(
        user_id=user.id,
        institute_id=institute.id,
    )

    db_session.add(membership)
    await db_session.commit()

    await db_session.refresh(membership)

    assert membership.user.id == user.id
    assert membership.institute.id == institute.id

