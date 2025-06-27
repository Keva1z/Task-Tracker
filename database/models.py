from datetime import datetime, timezone
from enum import Enum
from typing import Any

time_format = "%Y-%m-%dT%H:%M:%S"

class Status(Enum):
    NOT_DONE = 'not-done'
    IN_PROGRESS = 'in-progress'
    DONE = 'done'

class Task:
    _object_count = 0

    def __init__(self, description: str, *args, **kwargs):
        
        Task._object_count += 1
        self.id: int = self._object_count
        self.status: Status = Status.NOT_DONE
        self.description: str = description
        self.created_at: str = str(datetime.now())
        self.updated_at: str = self.created_at

        for key, value in kwargs.items():
            setattr(self, key, value)

    def __setattr__(self, name: str, value: Any) -> None:
        object.__setattr__(self, name, value)
        if name not in {"updated_at", "created_at"}:
            object.__setattr__(self, "updated_at", str(datetime.now()))

    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        return cls(
            description = data.get('description', ''),
            status = Status(data.get('status', 'not-done')),
            created_at = data.get('created_at', ''),
            updated_at = data.get('updated_at', '')
        )

    def to_dict(self) -> dict:
        return {
            'status': self.status.value,
            'description': self.description,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    def __str__(self) -> str:
        return f'{self.id}. {self.description} ({self.status.value})'
    
    def __repr__(self) -> str:
        # return f'Task(id={self.id})'
        return str(self)