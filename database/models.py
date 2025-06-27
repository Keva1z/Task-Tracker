from datetime import datetime, timezone
from enum import Enum

class Status(Enum):
    NOT_DONE = 'not-done'
    IN_PROGRESS = 'in-progress'
    DONE = 'done'

class Task:
    __task_count = 0

    def __init__(self, description: str, *args, **kwargs):
        
        Task.__task_count += 1
        self.id: int = self.__task_count
        self.status: Status = Status.NOT_DONE
        self.description: str = description
        self.created_at: str = str(datetime.now(timezone()))
        self.updated_at: str = self.created_at

    def to_dict(self) -> dict:
        return {}