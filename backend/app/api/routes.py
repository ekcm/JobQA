from fastapi import APIRouter, Depends
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

@router.get("/query")
async def query(query: QueryRequest, job_document: JobDocument = Depends(lambda: job_document_dependency)):

    retriever = VectorIndexRetriever(index=job_document.index, similarity_top_k=3)
    query_engine = RetrieverQueryEngine(retriever=retriever)
    response = query_engine.query(query.query)

    return {
        "query": query.query,
        "response": response
    }