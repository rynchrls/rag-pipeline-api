from fastapi import APIRouter
from app.v1.controller.pipeline import PipelineController


class PipelineRouter:
    def __init__(self):
        self.router = APIRouter()
        self.pipeline_controller = PipelineController()

        self.router.post("", status_code=201)(self.pipeline_controller.create_pipeline)


router = PipelineRouter().router
