from llama_index.core import (
    VectorStoreIndex,
)
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.vector_stores.pinecone import PineconeVectorStore
from pinecone import Pinecone

from app.core.config import settings

class JobRetriever:
    def __init__(self, index):
        self.index = index

    def retrieve_job(self, query: str):
        retriever = VectorIndexRetriever(index=self.index, similarity_top_k=3)
        query_engine = RetrieverQueryEngine(retriever=retriever)
        response = query_engine.query(query)

        return {
            "query": query,
            "response": response,
            "documents": response.source_nodes[0].text
        }

class ResumeRetriever:
    def retrieve_resume(self, query: str):
        pinecone_client = Pinecone(api_key=settings.PINECONE_API_KEY)
        pinecone_index = pinecone_client.Index(settings.PINECONE_INDEX_NAME)
        pinecone_vector_store = PineconeVectorStore(pinecone_index=pinecone_index)

        vector_index = VectorStoreIndex.from_vector_store(
            vector_store=pinecone_vector_store
        )

        retriever = VectorIndexRetriever(index=vector_index, similarity_top_k=3)
        response = retriever.retrieve(query)

        return {
            "query": query,
            "response": response[0].node.text,
        }
        