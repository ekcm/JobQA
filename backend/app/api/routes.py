from fastapi import APIRouter
from app.schemas.queries import JobContentRequest
from app.ingestion.job_ingestor import JobIngestor

router = APIRouter()

@router.get("/")
async def read_root():
    return {"message": "Hello World"}

@router.post("/job")
async def process_job(request: JobContentRequest):
    if request.job_link:
        # Fetch job content from the link
        ingestor = JobIngestor()
        job_content = ingestor.ingest(request.job_link)
        return {
            "message": f"Processing job link: {request.job_link}",
            "job_content": job_content
        }
    else:
        # Process the provided job content
        return {"message": f"Processing job content: {request.job_content[:30]}"}
    return {"message": "Job content"}