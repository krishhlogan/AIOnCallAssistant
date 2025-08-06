from fastapi import FastAPI, Request
from pydantic import BaseModel
from celery import Celery
import os
from worker import process_email


app = FastAPI()

celery = Celery(
    "worker",
    broker=os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0"),
    backend=os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")
)

class EmailRequest(BaseModel):
    subject: str
    sender: str
    body: str

@app.post("/submit-email")
def submit_email(payload: EmailRequest, llm_provider: str = "openai"):
    print('payload',payload)
    print('llm_provider',llm_provider)
    task = process_email.delay(payload.subject, payload.sender, payload.body, llm_provider)
    return {"message": "Email received and task scheduled", "task_id": task.id}
