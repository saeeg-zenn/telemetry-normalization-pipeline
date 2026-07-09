import uvicorn
from fastapi import FastAPI
from .routes import router

app = FastAPI(title="Governance Service")
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8001, reload=False)