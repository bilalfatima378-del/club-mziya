from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.company import Company
from app.models.subscription_plan import SubscriptionPlan
from app.schemas.company import CompanyCreate, CompanyRead, CompanyUpdate

router = APIRouter(prefix="/companies", tags=["Companies"])


def get_company_or_404(company_id: str, db: Session) -> Company:
    company = db.scalar(
        select(Company).where(Company.id == company_id, Company.is_active.is_(True))
    )
    if company is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Company not found"
        )
    return company


@router.post("", response_model=CompanyRead, status_code=status.HTTP_201_CREATED)
def create_company(payload: CompanyCreate, db: Session = Depends(get_db)) -> Company:
    if payload.plan_id is not None:
        plan = db.get(SubscriptionPlan, payload.plan_id)
        if plan is None or not plan.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid subscription plan",
            )

    existing = db.scalar(
        select(Company).where(Company.ice_number == payload.ice_number)
    )
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A company with this ICE number already exists",
        )

    company = Company(**payload.model_dump())
    db.add(company)
    db.commit()
    db.refresh(company)
    return company


@router.get("", response_model=list[CompanyRead])
def list_companies(db: Session = Depends(get_db)) -> list[Company]:
    return list(
        db.scalars(select(Company).where(Company.is_active.is_(True))).all()
    )


@router.get("/{company_id}", response_model=CompanyRead)
def get_company(company_id: str, db: Session = Depends(get_db)) -> Company:
    return get_company_or_404(company_id, db)


@router.patch("/{company_id}", response_model=CompanyRead)
def update_company(
    company_id: str,
    payload: CompanyUpdate,
    db: Session = Depends(get_db),
) -> Company:
    company = get_company_or_404(company_id, db)
    data = payload.model_dump(exclude_unset=True)

    if "plan_id" in data and data["plan_id"] is not None:
        plan = db.get(SubscriptionPlan, data["plan_id"])
        if plan is None or not plan.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid subscription plan",
            )

    if "ice_number" in data and data["ice_number"] != company.ice_number:
        duplicate = db.scalar(
            select(Company).where(Company.ice_number == data["ice_number"])
        )
        if duplicate is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A company with this ICE number already exists",
            )

    for field, value in data.items():
        setattr(company, field, value)

    db.commit()
    db.refresh(company)
    return company


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
def soft_delete_company(company_id: str, db: Session = Depends(get_db)) -> None:
    company = get_company_or_404(company_id, db)
    company.is_active = False
    db.commit()
