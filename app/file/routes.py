from fastapi import APIRouter,Depends ,HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_db
from app.file.models import File
from app.file.schemas import CompleteUploadModel, FileCreate,FileRead
from app.auth.dependencies import get_current_user
from app.auth.models import User
from app.utils import complete_upload  
from app.utils import generate_part_url, start_upload  

router = APIRouter()

@router.post("/start")
def start_multipart_upload(filename: str):
    return start_upload(filename)

@router.post("/presign-part")
def get_presigned_part_url(key: str, upload_id: str, part_number: int):
    return generate_part_url(key, upload_id, part_number)

@router.post("/",response_model=FileRead,status_code=status.HTTP_201_CREATED)
async def create(
    payload: CompleteUploadModel,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    # Finalize multipart upload to S3
    result = complete_upload(payload)  

    # Create DB record
    file_record = File(
        filename=payload.filename,
        file_type="application/octet-stream", 
        size=0,  
        extension=payload.filename.split(".")[-1],
        storage_url=result["location"],
        uploaded_by=current_user.id,
        dataset_id=payload.dataset_id,
    )

    db.add(file_record)
    await db.commit()
    await db.refresh(file_record)

    return file_record


