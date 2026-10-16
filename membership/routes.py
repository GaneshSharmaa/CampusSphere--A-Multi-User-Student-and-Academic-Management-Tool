from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth.dependencies import get_current_user
from database.dependencies import get_db
from membership.schemas import MembershipCreate, MembershipResponse
from membership.service import (
    create_membership,
    get_membership,
    get_user_memberships,
)
from users.models import User


router = APIRouter()


@router.post("/create", response_model=MembershipResponse)
async def create_membership_route(
    membership_data: MembershipCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await create_membership(db, membership_data, current_user)


@router.get("/me", response_model=list[MembershipResponse])
async def get_my_memberships(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await get_user_memberships(db, current_user)


@router.get("/{membership_id}", response_model=MembershipResponse)
async def get_membership_route(
    membership_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)],
):
    return await get_membership(db, membership_id, current_user)

