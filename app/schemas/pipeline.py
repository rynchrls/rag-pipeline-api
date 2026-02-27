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
    file_names: list[str]
    file_count: int
    stage: int

    @classmethod
    def as_form(
        cls,
        id: Optional[int] = Form(None),
        title: str = Form(...),
        description: str = Form(...),
        agent_name: str = Form(...),
        author_id: str = Form(...),
        email: str = Form(...),
        file_names: list[str] = Form(...),
        file_count: int = Form(...),
        stage: int = Form(...),
    ):
        # Form data may send list as a single comma-separated string
        # e.g. ["akali.md,ashe.md"] -> ["akali.md", "ashe.md"]
        parsed_file_names = []
        for name in file_names:
            parsed_file_names.extend(name.split(","))

        return cls(
            id=id,
            title=title,
            description=description,
            agent_name=agent_name,
            author_id=author_id,
            email=email,
            file_names=parsed_file_names,
            file_count=file_count,
            stage=stage,
        )


class GetPipeline(Pipeline):
    id: int
    author_id: int
