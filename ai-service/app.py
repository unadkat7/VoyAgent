from fastapi import FastAPI

app = FastAPI(
    title="VoyAgent AI Service",
    description="AI Service powered by LangGraph and LangChain",
    version="1.0.0"
)


@app.get("/")
async def health_check():
    return {
        "success": True,
        "message": "VoyAgent AI Service is running 🚀"
    }