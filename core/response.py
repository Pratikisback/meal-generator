# utils/response.py

from datetime import datetime, timezone

class Response:
    def __init__(self):
        self.status = "success"
        self.message = ""
        self.data = None
        self.status_code = None 

    def set(self, status: str = "success", status_code: int = 0,message: str = "", data=None):
        self.status = status
        self.status_code = status_code
        self.message = message
        self.data = data

        return self.dict()

    def dict(self):
        return {
            "status": self.status,
            "message": self.message,
            "status_code": self.status_code,
            "timestamp": str(datetime.now(timezone.utc)),
            "data": self.data,
        }
