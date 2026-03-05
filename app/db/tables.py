from app.models import user as User
from app.models import pipeline as Pipeline
from app.models import message as Message
from app.db.session import engine
from app.models import conversation as Conversation


def create_tables():
    User.Base.metadata.create_all(bind=engine)
    Pipeline.Base.metadata.create_all(bind=engine)
    Message.Base.metadata.create_all(bind=engine)
    Conversation.Base.metadata.create_all(bind=engine)
