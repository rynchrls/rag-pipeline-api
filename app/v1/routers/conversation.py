from fastapi import APIRouter
from app.v1.controller.conversation import ConversationController


class ConversationRouter:
    def __init__(self):
        self.router = APIRouter()
        self.conversation_controller = ConversationController()

        self.router.post("", status_code=201)(
            self.conversation_controller.create_conversation
        )
        self.router.get("", status_code=200)(
            self.conversation_controller.get_conversation
        )
        self.router.get("/all", status_code=200)(
            self.conversation_controller.get_all_conversations
        )


router = ConversationRouter().router
