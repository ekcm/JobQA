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

from app.core.config import settings

from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine

class JobIngestor:
    def __init__(self):
        self.chroma_client = chromadb.EphemeralClient()
        self.chroma_collection = self.chroma_client.create_collection("job_documents")
        self.vector_store = ChromaVectorStore(chroma_collection=self.chroma_collection)
        self.storage_context = StorageContext.from_defaults(vector_store=self.vector_store)
    
    def ingest_job(self, job_link: str = None, job_content: str = None):
        if job_link:
            document = SimpleWebPageReader(html_to_text=True).load_data(
                [job_link]
            )
            index = VectorStoreIndex(document, storage_context=self.storage_context)
        else:
            document = Document(text=job_content)
            index = VectorStoreIndex([document], storage_context=self.storage_context)


        return index


