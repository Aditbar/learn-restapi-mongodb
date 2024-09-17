from bson import ObjectId
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["tutorial"]
collection = db["todo"]

app = FastAPI()

class TodoModel(BaseModel):
  title: str = Field(...)
  description: str = Field(...)
  done: bool = False
  
# post todo
@app.post("/todo")
def create_todo(todo: TodoModel):
  
  todo = dict(todo)
  todo["_id"] = str(ObjectId())
  collection.insert_one(todo)
  return todo

@app.get("/todo")
def get_all_todos():
  todos = list(collection.find())
  for todo in todos:
    todo["_id"] = str(todo["_id"])
  return todos

@app.get("/todo/{id}")
def get_todo_by_id(id: str):
  todo = collection.find_one({"_id": id})
  if todo:
    todo["_id"] = str(todo["_id"])
    return todo
  else:
    raise HTTPException(status_code=404, 
                        detail="Todo not found")
    
@app.put("/todo/{id}")
def update_todo_by_id(id: str, todo: TodoModel):
  todo_data = todo.dict()
  update_todo_by_id = collection.find_one_and_update(
    {"_id": id},
    {"$set": todo_data}
  )
  if update_todo_by_id:
    return update_todo_by_id
  else:
    raise HTTPException(status_code=404,
                        detail="todo not found")
    
@app.delete("/todo/{id}")
def delete_todo_by_id(id: str):
  delete_todo_by_id = collection.find_one_and_delete({"_id": id})
  if delete_todo_by_id:
    return {"message": f"todo {id} deleted"}
  else:
    raise HTTPException(status_code=404,
                        detail="todo not found")
    
# update todo done
@app.put("/todo/{id}/done")
def mark_todo_as_done(id: str):
  todo = collection.find_one_and_update(
    {"_id": id}, {"$set": {"done": True}}
  )
  if todo:
    todo["_id"] = str(todo["_id"])
    return todo
  else:
    raise HTTPException(status_code=404,
                        detail="todo not found")