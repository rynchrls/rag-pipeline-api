from app.models import user as User
from app.models import pipeline as Pipeline
from app.db.session import engine


def create_tables():
    User.Base.metadata.create_all(bind=engine)
    Pipeline.Base.metadata.create_all(bind=engine)
