
from fastapi import APIRouter, Depends ,HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_db
from app.datasets.models import Dataset
from app.datasets.schemas import DatasetCreate,DatasetRead

router= APIRouter()

@router.post("/",response_model=DatasetRead,status_code+status.HTTP_201_CREATED)
async def create(dataset:DatasetCreate,current_user: User = Depends(get_current_user)
,db:AsyncSession=Depends(get_db)):
      new_dataset = Dataset(
        title=dataset.title,
        tags=dataset.tags,
        metadata=dataset.metadata,
        user_id=current_user.id
    )

    db.add(new_dataset)
    await db.commit()
    await db.refresh(new_dataset)

    return new_dataset
   
@router.get("/",response_model=DatasetRead,status_code=status,HTTP_200_OK)
async def findAll(current_user:User = Depends(get_current_user)):
    results = await db.execute(select(Dataset).where(Dataset.user_id == current_user.id))
    datasets = result.scalars().all()

    if not datasets:
        raise HTTPException(
            status_code=status.HTTP_404_NOTFOUND,
            details = "Datasets not found for this user"
        )

    return datasets


@router.get("/{id}")
async def findOne(current_user:User = Depends(get_current_user)):
    result = await db.execute(select(Dataset).where(Dataset.id == id and Dataset.user_id == current_user.id ) )
    dataset = result.scalars_one_or_none()

    if not dataset:
        raise HTTPException(
            status_code=status.HTTP_404_NOTFOUND,
            details = "Dataset not found for this user"
        )




@router.put()
async def update():

@router.delete()
async def delete():        

