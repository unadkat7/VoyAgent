from fastapi import FastAPI
from api.planner import router as planner_router

app = FastAPI(
    title="VoyAgent AI Service",
    description="AI Backend for VoyAgent",
    version="1.0.0",
)

app.include_router(
    planner_router,
    prefix="/planner",
    tags=["Planner"],
)

@app.get("/")
def home():
    return {
        "success": True,
        "message": "VoyAgent AI Service is Running 🚀",
    }
