from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.tables import create_tables
from app.v1.routers import user
from app.v1.routers import pipeline

create_tables()

app = FastAPI(
    title="Rag Pipeline",
    version="1.0.0",
    description="Create your own AI Agent/Assistant without coding.",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ✅ CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ✅ TEMPORARY: Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ✅ Optional root route
@app.get("/")
def read_root():
    return {"message": "Welcome to RAG Pipeline"}


# ✅ Register API routes
app.include_router(user.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(pipeline.router, prefix="/api/v1/pipelines", tags=["Pipelines"])
