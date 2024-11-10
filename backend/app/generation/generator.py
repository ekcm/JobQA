from openai import OpenAI
from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

class GenerateAnswer:
    def generate_answer(self, query: str, job_document: str, resume_document: str):
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a career advisor helping a job seeker."},
                {"role": "user", "content": f'''
                    You are to answer a question from a job seeker who is looking for a job.
                    The job seeker has a job document and a resume document.
                    Answer the question based on the job document and the resume document.
                    The job document is as follows:
                    {job_document}
                    The resume document is as follows:
                    {resume_document}
                    The question is:
                    {query}
                '''
                }
            ]
        )
        return completion.choices[0].message.content