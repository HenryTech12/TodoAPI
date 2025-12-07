#crud operations

from fastapi import Depends, HTTPException, status
from schemas import schema
from db import db
import logging

from model import models

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


models.db.Base.metadata.create_all(db.engine)


def create_todo(todo , db):
    if todo:
        todo_db = db.query(models.Todo).filter(models.Todo.id == todo.id).first()
        if(todo_db):
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"data with id:{todo.id} already exists")
        else:
            todo_db = models.Todo(id = todo.id, completed = todo.completed, item = todo.item)
            db.add(todo_db)
            db.commit()
            db.refresh(todo_db)
            
            logger.info("data saved to db.")
            
            return todo_db
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Invalid Data")


def get_all(db):
    todo_list = db.query(models.Todo).all()
    if todo_list:
        return todo_list
    else:
        logger.error("data not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data Not Found")

def get_by_id(id, db):
    todo_res = db.query(models.Todo).filter(models.Todo.id == id).first() 
    if todo_res:
        logger.info(f"data with id: {id} fetched from db.")
        return todo_res
    else:
        logger.error("data not found..")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = 'Data Not Found')
    
def update_by_id(id, todo, db):
    todo_db = db.query(models.Todo).filter(models.Todo.id == id).first()
    if todo_db:
        if todo.item:
            todo_db.item = todo.item
        if todo.completed:
            todo_db.completed = todo.completed
            
        db.commit()
        db.refresh(todo_db)
        
        logger.info(f"data with id: {id} updated")
        return todo_db
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data not found")
    
def delete_by_id(id,db):
    todo_db = db.query(models.Todo).filter(models.Todo.id == id).first()
    if todo_db:
        db.delete(todo_db)
        db.commit()
        
        logger.info(f"data with id: {id} removed from db")
        return todo_db
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f'data with id: {id} not found')
    
        
def get_page(page, size, db):
    skip = (page - 1) * size
    todo_page = db.query(models.Todo).offset(skip).limit(size).all()
    if not todo_page:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "no data found")
    else:
        paginated_response = schema.PaginatedTodo(page=page, size = size, data=todo_page)
        return paginated_response;
