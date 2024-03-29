import uvicorn
from fastapi import FastAPI

from app.controllers.job_controller import job_router
from app.controllers.model_controller import model_router
from app.controllers.training_controller import router

app = FastAPI()

app.include_router(router)
app.include_router(model_router)
app.include_router(job_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
