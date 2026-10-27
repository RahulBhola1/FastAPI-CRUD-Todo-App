from fastapi import FastAPI , Depends , HTTPException
from database import Base , engine , SessionLocal
import models 
from sqlalchemy.orm import Session
from schemas import ToDoCreate , ToDoResponse

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/todos/" , response_model= ToDoResponse)
def create_todo (obj : ToDoCreate , db : Session = Depends(get_db)):
    todo = models.ToDo(title = obj.title , completed = obj.completed)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return(todo)

@app.get("/todos" , response_model=list[ToDoResponse])
def get_todos(db:Session=Depends(get_db)):
    objs = db.query(models.ToDo).all()
    return objs

@app.get("/todos/{todo_id}" , response_model=ToDoResponse)
def get_todos(todo_id:int , db:Session=Depends(get_db)):
    obj = db.query(models.ToDo).filter(models.ToDo.id== todo_id). first()
    if obj is None:
        raise HTTPException(status_code=404 , detail="Record Not Found ")
    return obj

@app.put("/todos/{todo_id}",response_model=ToDoResponse)
def update_todo(todo_id:int,new_data:ToDoCreate,db:Session=Depends(get_db)):
    obj=db.query(models.ToDo).filter(models.ToDo.id==todo_id).first()
    if obj is None:
        raise HTTPException(status_code=404,detail="Record not found")
    obj.title=new_data.title
    obj.completed=new_data.completed
    db.commit()
    db.refresh(obj)
    return obj

@app.delete("/todos/{todo_id}")
def update_todo(todo_id:int,db:Session=Depends(get_db)):
    obj=db.query(models.ToDo).filter(models.ToDo.id==todo_id).first()
    if obj is None:
        raise HTTPException(status_code=404,detail="Record not found")
    db.delete(obj)
    db.commit()
    return {"msg":"Record Deleted successfully"}
