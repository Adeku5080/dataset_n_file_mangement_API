from fastapi import APIRouter, Depends, HTTPException, status,Query
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.datasets.models import Dataset
from app.datasets.schemas import DatasetCreate, DatasetRead
from app.auth.models import User

router = APIRouter()


@router.post("/", response_model=DatasetRead, status_code=status.HTTP_201_CREATED)
async def create(
    dataset: DatasetCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    
    existing = await db.execute(
        select(Dataset).where(
            (Dataset.user_id == current_user.id) &
            (Dataset.title == dataset.title)
        )
    )

    if existing.scalar_one_or_none():
         raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Dataset with this title already exists"
        )
   
    new_dataset = Dataset(
        title=dataset.title,
        tags=dataset.tags,
        user_id=current_user.id,
        dataset_metadata=dataset.dataset_metadata
    )

    db.add(new_dataset)
    await db.commit()
    await db.refresh(new_dataset)

    return new_dataset

@router.get("/", response_model=list[DatasetRead], status_code=status.HTTP_200_OK)
async def findAllUserDatasets(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    results = await db.execute(select(Dataset).where(Dataset.user_id == current_user.id))
    datasets = results.scalars().all()

    if not datasets:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Datasets not found for this user"
        )

    return datasets

@router.get("/{id}", response_model=DatasetRead)
async def findOne(
    id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Dataset).where(
            (Dataset.id == id) & (Dataset.user_id == current_user.id)
        )
    )
    dataset = result.scalars().first()

    if not dataset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset not found for this user"
        )
    
    return dataset

@router.put("/{id}", response_model=DatasetRead)
async def update(
    id: int,
    dataset: DatasetCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Update implementation here
    pass

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Delete implementation here
    pass


@router.get("/search", status_code=status.HTTP_200_OK)
async def search_datasets(
    q: str = Query(..., min_length=1),
    db: AsyncSession = Depends(get_db)
):
    stmt = text("""
        SELECT * FROM datasets
        WHERE search_vector @@ phraseto_tsquery(:query)
        ORDER BY ts_rank(search_vector, plainto_tsquery(:query)) DESC
    """)
    result = await db.execute(stmt, {"query": q})
    rows = result.mappings().all()  # this gives you dicts instead of tuples
    return rows
