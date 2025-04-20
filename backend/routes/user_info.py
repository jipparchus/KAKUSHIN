from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.schemas import UserProfile
from db.models import User
from db.dependency import get_db
from auth.dependencies import get_current_user
router = APIRouter()


@router.get("/profile")
def get_profile(current_user: User = Depends(get_current_user)):
    print('***********************')
    print(current_user.username)
    print('***********************')
    return current_user


@router.put("/profile")
def update_profile(
    data: UserProfile,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Endpoint to insert the usedr info.
    current_user is already tracked by the session in get_current_user
    """
    current_user.v_grade = data.v_grade
    current_user.height = data.height
    current_user.weight = data.weight
    current_user.share_info = data.share_info
    db.commit()  # generate an UPDATE SQL statement only for the fields that changed.
    db.refresh(current_user)
    return current_user
    # return {"status": "updated"}
