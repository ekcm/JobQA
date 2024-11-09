from fastapi import APIRouter
from app.schemas.queries import JobContentRequest

router = APIRouter()

from pydantic import BaseModel, root_validator
from typing import Optional

class JobContentRequest(BaseModel):
    job_link: Optional[str] = None
    job_content: Optional[str] = None

    @root_validator(pre=True)
    def check_mutually_exclusive(cls, values):
        if bool(values.get('job_link')) == bool(values.get('job_content')):
            raise ValueError('Exactly one of job_link or job_content must be provided')
        return values

@router.get("/")
async def read_root():
    return {"message": "Hello World"}

@router.post("/job")
async def process_job(request: JobContentRequest):
    if request.job_link:
        # Fetch job content from the link
        return {"message": f"Processing job link: {request.job_link}"}
    else:
        # Process the provided job content
        return {"message": f"Processing job content: {request.job_content[:30]}"}
    return {"message": "Job content"}