from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    docs="/",
)
app.include_router(router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)