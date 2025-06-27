import pathlib, json
from database.models import Task

class JSONDatabase():
    __path: str = pathlib.Path("database/tasks.json")
    __objects: dict[int, Task] = {}

    def __init__(self) -> None:
        self.__load()

    def put(self, task: Task) -> None:
        self.__objects[task.id] = task
    
    def get(self, key: int|None = None) -> Task|list[Task]|None:
        if key is not None: return self.__objects[key] if key in self.__objects else None
        return list(self.__objects.values())
    
    def update(self, task: Task) -> None:
        if task.id in self.__objects:
            self.__objects[task.id] = task

    def delete(self, key: int) -> Task|None:
        if key in self.__objects:
            if Task._object_count > key:
                change = False
                for obj_key, task in self.__objects.items():
                    if obj_key > key: change = True
                    if change:
                        task.id -= 1
                        self.__objects[obj_key-1] = task
            object = self.__objects.pop(Task._object_count)
            Task._object_count -= 1
            return object
        return None

    def save(self) -> None:
        with open(self.__path, 'w+', encoding='UTF-8') as f:
            objects = {}
            for key, task in self.__objects.items(): objects[key] = task.to_dict()
            f.write(json.dumps(objects, indent=4))

    def __load(self) -> None:
        with open(self.__path, 'r+', encoding='UTF-8') as f:
            try:
                objects: dict[int, str] = json.loads(f.read())
                for key, object in objects.items():
                    self.__objects[int(key)] = Task.from_dict(object)
            except:
                pass