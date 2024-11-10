from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from app.schemas.queries import JobContentRequest, QueryRequest
from app.ingestion.job_ingestor import JobIngestor

from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine

router = APIRouter()

class JobDocument:
    def __init__(self):
        self.index = None

job_document_dependency = JobDocument()

@router.post("/job")
async def process_job(request: JobContentRequest, job_document: JobDocument = Depends(lambda: job_document_dependency)):
    ingestor = JobIngestor()
    if request.job_link:
        message = f"Processing job link: {request.job_link}"
        job_document.index = ingestor.ingest_job(request.job_link)
    else:
        message = f"Processing job content"
        job_document.index = ingestor.ingest_job(job_content=request.job_content)

    return {
        "message": message,
    }

@router.post("/resume")
async def process_resume(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are supported"
        )

    ingestor = JobIngestor()
    result = ingestor.ingest_resume(file)

    if result.get("status")== "success":
        return {
            "status": result["status"],
            "message": result["message"]
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=result["message"]
        )

@router.get("/query")
async def query(query: QueryRequest, job_document: JobDocument = Depends(lambda: job_document_dependency)):
    if not job_document.index:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No job document found. Please ingest a job document first."
        )

    retriever = VectorIndexRetriever(index=job_document.index, similarity_top_k=3)
    query_engine = RetrieverQueryEngine(retriever=retriever)
    response = query_engine.query(query.query)

    return {
        "query": query.query,
        "response": response
    }