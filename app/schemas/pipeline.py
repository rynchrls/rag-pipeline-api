from pydantic import BaseModel
from typing import Optional, Any
from fastapi import Form
import json


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
    rp_metadata: Optional[dict[str, Any]] = None
    chunks_count: Optional[int] = None

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
        rp_metadata: Optional[str] = Form(None),
        chunks_count: Optional[int] = Form(None),
    ):
        # Form data may send list as a single comma-separated string
        # e.g. ["akali.md,ashe.md"] -> ["akali.md", "ashe.md"]
        parsed_file_names = []
        for name in file_names:
            parsed_file_names.extend(name.split(","))
        parsed_rp_metadata = None
        if rp_metadata:
            try:
                parsed_rp_metadata = json.loads(rp_metadata)
            except json.JSONDecodeError:
                # Handle or log error if needed, for now we set it as is or empty
                parsed_rp_metadata = {}

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
            rp_metadata=parsed_rp_metadata,
            chunks_count=chunks_count,
        )


class GetPipeline(Pipeline):
    id: int
    author_id: int


class GetAllPipelines(BaseModel):
    author_id: int
    page: int
    limit: int
    search: Optional[str] = None
