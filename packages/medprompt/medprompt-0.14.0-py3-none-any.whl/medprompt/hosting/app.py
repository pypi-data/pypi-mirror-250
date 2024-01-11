import sys
import logging
from fastapi import FastAPI, APIRouter
import uvicorn
from .base_server import BaseServer
from .base_model import BaseModel

_model: BaseModel = None
_server: BaseServer = None
# Set up logger
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
log = logging.getLogger(__name__)

app = FastAPI()
router = APIRouter()

@router.get("/")
async def home():
    return {"message": "Machine Learning service"}

@router.post("/predict")
async def data(data: dict):
    return _server.predict(data)

@router.get("/health")
async def health():
    return _server.health_check()


app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("app:app", reload=True, port=8080, host="0.0.0.0")