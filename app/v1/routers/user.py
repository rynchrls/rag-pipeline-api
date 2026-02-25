from fastapi import APIRouter
from app.v1.controller.user import UserController


class UserRouter:
    def __init__(self):
        self.router = APIRouter()
        self.user_controller = UserController()

        self.router.post("", status_code=201)(self.user_controller.create_user)
        self.router.post("/login", status_code=200)(self.user_controller.login_user)


router = UserRouter().router
