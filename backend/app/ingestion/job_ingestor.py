from llama_index.readers.web import SimpleWebPageReader
from llama_index.core import (
    Document,
    load_index_from_storage,
    VectorStoreIndex,
    StorageContext
)
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.extractors import TitleExtractor
from llama_index.core.ingestion import IngestionPipeline
import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.vector_stores.pinecone import PineconeVectorStore
from pinecone import Pinecone
import pdfplumber

from app.core.config import settings

class JobIngestor:
    def __init__(self):
        self.chroma_client = chromadb.EphemeralClient()
        self.chroma_collection = self.chroma_client.create_collection("job_documents")
        self.chroma_vector_store = ChromaVectorStore(chroma_collection=self.chroma_collection)
        self.chroma_storage_context = StorageContext.from_defaults(vector_store=self.chroma_vector_store)
    
    def ingest_job(self, job_link: str = None, job_content: str = None):
        if job_link:
            document = SimpleWebPageReader(html_to_text=True).load_data(
                [job_link]
            )
            index = VectorStoreIndex(document, storage_context=self.chroma_storage_context)
        else:
            document = Document(text=job_content)
            index = VectorStoreIndex([document], storage_context=self.chroma_storage_context)

        return index

    def ingest_resume(self, file):
        try:
            resume_content = ''
            with pdfplumber.open(file.file) as pdf:
                for page in pdf.pages:
                    resume_content += page.extract_text()

            resume_document = Document(text=resume_content)

            pinecone_client = Pinecone(api_key=settings.PINECONE_API_KEY)
            pinecone_index = pinecone_client.Index(settings.PINECONE_INDEX_NAME)
            pinecone_vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
            pinecone_storage_context = StorageContext.from_defaults(vector_store=pinecone_vector_store)

            resume_index = VectorStoreIndex.from_documents(
                [resume_document],
                storage_context=pinecone_storage_context
            )

            return {
                "status": "success",
                "message": "Resume ingested into Pinecone successfully"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

