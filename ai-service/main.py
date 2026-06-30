from fastapi import FastAPI

app = FastAPI(
    title="VoyAgent AI Service",
    description="AI Backend for VoyAgent",
    version="1.0.0",
)


@app.get("/")
def home():
    return {
        "success": True,
        "message": "VoyAgent AI Service is Running 🚀",
    }