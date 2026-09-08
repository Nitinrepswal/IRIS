import logging
from fastapi import FastAPI
from pydantic import BaseModel

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("iris")

app = FastAPI(title="IRIS Production Backend")


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def root():
    logger.info("Root endpoint requested")
    return {"name": "IRIS", "status": "running"}


@app.get("/health")
def health():
    logger.info("Health check requested")
    return {"status": "healthy"}


@app.post("/chat")
def chat(request: ChatRequest):
    logger.info("Chat request received")

    response = f"IRIS received: {request.message}"

    logger.info("Chat response generated")

    return {"response": response}