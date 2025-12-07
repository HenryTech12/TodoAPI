from fastapi import FastAPI, HTTPException, status, Depends
from schemas import schema
from typing import List
from db import db
from service import service
from sqlalchemy.orm import Session

app = FastAPI()


#create todod
@app.post('/api/todo', response_model=schema.Todo, status_code=status.HTTP_201_CREATED)
def create_todo(todo: schema.Todo, db: Session= Depends(db.getdb)):
    print("hello")
    return service.create_todo(todo, db)

@app.get("/api/todo", status_code=status.HTTP_200_OK)
def getTodos(db: Session= Depends(db.getdb)):
    return service.get_all(db)

@app.get("/api/todo/{id}", response_model=schema.Todo, status_code=status.HTTP_200_OK)
def get_by_id(id: int, db: Session = Depends(db.getdb)):
    print(id)
    
    return service.get_by_id(id,db)

@app.patch("/api/todo/{id}")
def update_by_id(id: int, todo: schema.Todo, db: Session = Depends(db.getdb)):
    return service.update_by_id(id,todo,db)

@app.delete("/api/todo/{id}")
def delete_by_id(id: int, db: Session = Depends(db.getdb)):
    return service.delete_by_id(id,db)


@app.get("/api/todo")
def get_page(page: int = 1, size: int = 10, db: Session = Depends(db.getdb)):
    return service.get_page(page,size,db)