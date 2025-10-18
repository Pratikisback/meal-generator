from celery import Celery
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
celery = Celery(
    'tasks',
    broker='amqp://guest:guest@rabbitmq',
    backend=DATABASE_URL
)
@celery.task
def example_task():
    # Simulate a long-running task
    import time
    time.sleep(10)
    return "Task completed"