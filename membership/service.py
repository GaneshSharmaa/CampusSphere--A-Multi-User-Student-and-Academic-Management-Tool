from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from institutes.models import Institute
from membership.models import Membership
from membership.schemas import MembershipCreate
from users.models import User


async def create_membership(
    db: AsyncSession,
    membership_data: MembershipCreate,
    current_user: User,
) -> Membership:
    institute = await db.scalar(
        select(Institute).where(Institute.id == membership_data.institute_id)
    )
    if institute is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Institute not found.",
        )

    existing_membership = await db.scalar(
        select(Membership).where(
            Membership.user_id == current_user.id,
            Membership.institute_id == membership_data.institute_id,
        )
    )
    if existing_membership is not None:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "User is already a member of this institute.",
        )

    membership = Membership(
        user_id = current_user.id,
        institute_id = membership_data.institute_id,
    )
    db.add(membership)

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "User is already a member of this institute.",
        ) from None

    await db.refresh(membership)
    membership.institute = institute
    return membership


async def get_user_memberships(
    db: AsyncSession,
    current_user: User,
) -> list[Membership]:
    result = await db.scalars(
        select(Membership)
        .options(selectinload(Membership.institute))
        .where(Membership.user_id == current_user.id)
        .order_by(Membership.id)
    )
    return list(result.all())


async def get_membership(
    db: AsyncSession,
    membership_id: int,
    current_user: User,
) -> Membership:
    membership = await db.scalar(
        select(Membership)
        .options(selectinload(Membership.institute))
        .where(
            Membership.id == membership_id,
            Membership.user_id == current_user.id,
        )
    )
    if membership is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Membership not found.",
        )

    return membership

