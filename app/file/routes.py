from fastapi import APIRouter,Depends ,HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_db
from app.file.models import File
from app.file.schema import FileCreate,FileRead

router = APIRouter()

@router.post("/",response_model=FileRead,status_code=status.HTTP_201_CREATED)
async def create(file:fileCreate,datasetId,current_user:User = Depends(get_current_user)):
    # i will check dataset table to make sure dataset.userId = userIde
    # then call upload 
    



@router.get("/{datasetId}",response_model=FileRead,status_code=status.HTTP_200_OK)
async def findAllUserFilesInDataset():

