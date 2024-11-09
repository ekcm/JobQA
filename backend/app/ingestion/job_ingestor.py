from llama_index.readers.web import SimpleWebPageReader
from llama_index.core import Document

class JobIngestor:
    def ingest_job(self, job_link: str = None, job_content: str = None):
        if job_link:
            web_document = SimpleWebPageReader(html_to_text=True).load_data(
                [job_link]
            )
            return web_document
        else:
            return Document(content=job_content)