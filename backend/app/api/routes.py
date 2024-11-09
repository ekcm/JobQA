from fastapi import APIRouter
from app.schemas.queries import JobContentRequest
from app.ingestion.job_ingestor import JobIngestor

router = APIRouter()

@router.get("/")
async def read_root():
    return {"message": "Hello World"}

@router.post("/job")
async def process_job(request: JobContentRequest):
    ingestor = JobIngestor()
    if request.job_link:
        message = f"Processing job link: {request.job_link}"
        job_content = ingestor.ingest_job(request.job_link)
    else:
        message = f"Processing job content"
        job_content = ingestor.ingest_job(job_content=request.job_content)

    return {
        "message": message,
        "job_content": job_content
    }