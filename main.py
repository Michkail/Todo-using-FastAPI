from typing import Optional, List
from fastapi import FastAPI
from todo_using_fastapi.models.models import Todo, Todo_Pydantic, TodoIn_Pydantic
from pydantic import BaseModel
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise

app = FastAPI()

@app.get("/")
async def read_root():
    return {
        "hello": "aw"
    }

class Status(BaseModel):
    message: str

#R on CRUD is Retrieve
@app.get("/todos", response_model=List[Todo_Pydantic])
async def get_todos():
    return await Todo_Pydantic.from_queryset(
        Todo.all()
    )

#C on CRUD is Create
@app.post("/todos", response_model=Todo_Pydantic)
async def create_todo(todo: TodoIn_Pydantic):
    todo_obj = await Todo.create(
        **todo.dict(
            exclude_unset=True
        )
    )
    return await Todo_Pydantic.from_tortoise_orm(todo_obj)

@app.get("/todos/{todo_id}", response_model=Todo_Pydantic, responses={
    404: {
        "model": HTTPNotFoundError
    }
})
async def get_todo(todo_id: int):
    return await Todo_Pydantic.from_queryset_single(
        Todo.get(
            id=todo_id
        )
    )

@app.put("/todos/{todo_id}", response_model=Todo_Pydantic, responses={
    404: {
        "model": HTTPNotFoundError
    }
})
async def udpate_todo(todo_id: int, todo:Todo_Pydantic):
    await Todo.filter(id=todo_id).update(
        **todo.dict(
            exclude={
                "id"
            },
            exclude_unset=True
        )
    )
    return await Todo_Pydantic.from_queryset_single(
        Todo.get(
            id=todo_id
        )
    )

@app.delete("/todos/{todo_id}", response_model=Status, responses={
    404: {
        "model": HTTPNotFoundError
    }
})
async def delete_todo(todo_id: int):
    delete_count = await Todo.filter(id=todo_id).delete()
    if not delete_count:
        raise HTTPException(
            status_code=404,
            detail=f"Todo {todo_id} does not exist"
        )
    return Status(message=f"Deleted todo {todo_id}")

register_tortoise(
    app,
    db_url = "postgres://postgres:sru@localhost:5432/todo_fastapi",
    modules = {
        "models": [
            "todo_using_fastapi.models.models"
        ]
    },
    generate_schemas=True,
    add_exception_handlers=True
)