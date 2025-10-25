from main import celery
@celery.task
def example_task():
    # Simulate a long-running task
    import time
    time.sleep(10)
    return "Task completed"