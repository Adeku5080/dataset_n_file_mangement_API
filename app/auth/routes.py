from fastapi import APIRouter, Depends ,HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserRead
from app.auth.utils import hash_password,create_access_token

router = APIRouter()

@router.post("/signup",response_model= UserRead,status_code=status.HTTP_201_CREATED)
async def signup(user:UserCreate,db:AsyncSession=Depends(get_db)):
    # check if user already exists 
    result = await db.execute(select(User).where(User.email == user.email))
    existing_user = result.scalar()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    new_user = User(
        full_name = user.full_name ,
        email = user.email,
        password = hash_password(user.password)       
    )    

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    token = create_access_token(data={"sub": new_user.email})

    return {
        "id": new_user.id,
        "username": new_user.full_name,
        "email": new_user.email,
        "access_token": token,
        "token_type": "bearer"
    }
