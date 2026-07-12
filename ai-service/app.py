from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.planner import router as planner_router

app = FastAPI(
    title="VoyAgent AI Service",
    description="AI Backend for VoyAgent",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
