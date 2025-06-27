import os, json

class database():
    __path: str = os.path.expanduser("~/tasks.json")
    __objects: dict[str, str] = {}

    def __init__(self) -> None:
        pass

    def put(self, key: str, object) -> None:
        pass
    
    def get(self, key: str) -> str|None:
        return self
    
    def update(self, key: str) -> None:
        pass