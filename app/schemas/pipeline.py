from pydantic import BaseModel
from typing import Optional
from fastapi import Form


class Pipeline(BaseModel):
    id: Optional[int] = None
    title: str
    agent_name: str
    description: str
    author_id: int


class CreatePipeline(Pipeline):
    email: str

    @classmethod
    def as_form(
        cls,
        title: str = Form(...),
        description: str = Form(...),
        agent_name: str = Form(...),
        author_id: str = Form(...),
        email: str = Form(...),
    ):
        return cls(
            title=title,
            description=description,
            agent_name=agent_name,
            author_id=author_id,
            email=email,
        )
