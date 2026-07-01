from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="SHL AI Assessment Recommendation Agent",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message": "SHL AI Assessment Recommendation Agent",
        "docs": "/docs",
        "health": "/health"
    }

app.include_router(router)