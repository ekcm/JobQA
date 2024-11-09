from pydantic import BaseModel, root_validator, HttpUrl
from typing import Optional

class JobContentRequest(BaseModel):
    job_link: Optional[str] = None
    job_content: Optional[str] = None

    @root_validator(pre=True)
    def check_mutually_exclusive(cls, values):
        if bool(values.get('job_link')) == bool(values.get('job_content')):
            raise ValueError('Exactly one of job_link or job_content must be provided')
        return values