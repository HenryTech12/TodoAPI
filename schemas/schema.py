from pydantic import BaseModel

class Todo(BaseModel):
    id: int
    completed: bool
    item: str
    
class PaginatedTodo(BaseModel):
    page: int
    size: int
    data: Todo