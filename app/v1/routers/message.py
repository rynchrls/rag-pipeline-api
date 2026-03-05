from fastapi import APIRouter
from app.v1.controller.message import MessageController


class MessageRouter:
    def __init__(self):
        self.router = APIRouter()
        self.message_controller = MessageController()

        self.router.post("", status_code=201)(self.message_controller.create_message)
        self.router.post("/llm", status_code=201)(
            self.message_controller.save_llm_message
        )
        self.router.get("/all", status_code=201)(
            self.message_controller.get_all_messages
        )


router = MessageRouter().router
