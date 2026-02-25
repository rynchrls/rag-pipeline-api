import uvicorn
from dotenv import load_dotenv
from app.config import settings

load_dotenv()

host = settings.HOST
port = settings.PORT
debug = settings.DEBUG

if __name__ == "__main__":
    uvicorn.run("app.main:app", host=host, port=port, reload=debug, log_level="info")
