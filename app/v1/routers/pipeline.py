from fastapi import APIRouter
from app.v1.controller.pipeline import PipelineController


class PipelineRouter:
    def __init__(self):
        self.router = APIRouter()
        self.pipeline_controller = PipelineController()

        self.router.post("", status_code=201)(self.pipeline_controller.create_pipeline)
        self.router.get("", status_code=200)(self.pipeline_controller.get_pipeline)
        self.router.patch("", status_code=201)(self.pipeline_controller.update_pipeline)
        self.router.get("/all", status_code=200)(
            self.pipeline_controller.get_all_pipelines
        )
        self.router.delete("", status_code=200)(
            self.pipeline_controller.delete_pipeline
        )


router = PipelineRouter().router
