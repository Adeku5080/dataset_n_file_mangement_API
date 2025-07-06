from fastapi import APIRouter, Depends ,HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserRead,UserLogin
from app.auth.utils import hash_password,create_access_token,verify_password

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
        fullname = user.fullname ,
        email = user.email,
        password = hash_password(user.password)       
    )    

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    token = create_access_token(data={"sub": new_user.email})
    print(token)

    return {
        "id": new_user.id,
        "fullname": new_user.fullname,
        "email": new_user.email,
        "access_token": token,
        "token_type": "bearer"
    }

@router.post("/login",response_model= UserRead,status_code=status.HTTP_200_OK)
async def login(userCredentials:UserLogin,db:AsyncSession=Depends(get_db)):
        result = await db.execute(select(User).where(User.email == userCredentials.email))
        user = result.scalar_one_or_none()

        if not user or not verify_password(userCredentials.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        token = create_access_token({"sub": user.email})
        return {
            "id": user.id,
            "fullname": user.fullname,
            "email": user.email,
            "access_token": token,
            "token_type": "bearer"
       }


        





