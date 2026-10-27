from pydantic import BaseModel

class ToDoCreate (BaseModel):
    title : str
    completed : bool=False

class ToDoResponse (ToDoCreate):
    id : int 
    class Config :
        from_attribures = True