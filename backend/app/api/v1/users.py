from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.company import Company
from app.models.merchant import Merchant
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])


def hash_password(password: str) -> str:
    # Sprint 1 placeholder. Replace with bcrypt/passlib in the authentication sprint.
    return f"temporary-hash::{password}"


def get_user_or_404(user_id: str, db: Session) -> User:
    user = db.scalar(
        select(User).where(User.id == user_id, User.is_active.is_(True))
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


def validate_tenant(
    company_id: str | None, merchant_id: str | None, db: Session
) -> None:
    if company_id is not None:
        company = db.get(Company, company_id)
        if company is None or not company.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid company"
            )

    if merchant_id is not None:
        merchant = db.get(Merchant, merchant_id)
        if merchant is None or not merchant.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid merchant"
            )


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, db: Session = Depends(get_db)) -> User:
    validate_tenant(payload.company_id, payload.merchant_id, db)

    existing = db.scalar(select(User).where(User.email == payload.email))
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email already registered"
        )

    user = User(
        **payload.model_dump(exclude={"password"}),
        password_hash=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get("", response_model=list[UserRead])
def list_users(db: Session = Depends(get_db)) -> list[User]:
    return list(db.scalars(select(User).where(User.is_active.is_(True))).all())


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: str, db: Session = Depends(get_db)) -> User:
    return get_user_or_404(user_id, db)


@router.patch("/{user_id}", response_model=UserRead)
def update_user(
    user_id: str,
    payload: UserUpdate,
    db: Session = Depends(get_db),
) -> User:
    user = get_user_or_404(user_id, db)
    data = payload.model_dump(exclude_unset=True)

    validate_tenant(data.get("company_id"), data.get("merchant_id"), db)

    if "email" in data and data["email"] != user.email:
        duplicate = db.scalar(select(User).where(User.email == data["email"]))
        if duplicate is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Email already registered"
            )

    password = data.pop("password", None)
    for field, value in data.items():
        setattr(user, field, value)

    if password is not None:
        user.password_hash = hash_password(password)

    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def soft_delete_user(user_id: str, db: Session = Depends(get_db)) -> None:
    user = get_user_or_404(user_id, db)
    user.is_active = False
    db.commit()
