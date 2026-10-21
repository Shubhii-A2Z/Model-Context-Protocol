import json
from pathlib import Path
from datetime import timezone
from datetime import datetime
from typing import Literal
from fastmcp import FastMCP
from pydantic import BaseModel

mcp=FastMCP(
    name="Todo",
    instructions=(
        "A simple todo list. Use create_todo, list_todo, delete_todo, "
        "get_todo and update_todo to manage your todos"
    )
)

Status=Literal["pending", "completed", "deleted"]

# Local file to store todos
STORE_TODOS=Path(__file__).with_name("todos.json")


class Todo(BaseModel):
    id: str
    title: str
    status: Status="pending"
    description: str=""
    created_at: str
    updated_at: str


def _now()->str:
    """
    Returns current UTC timestamp
    """

    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _load_todos()->dict[str, Todo]:
    """
    Loading all todos from local file.
    """

    if not STORE_TODOS.exists():
        return {}
    
    raw=json.loads(STORE_TODOS.read_text()) or "[]"
    return {item["id"]: Todo.model_validate(item) for item in raw}


def _save(todos: dict[str, Todo])->None:
    """
    Saving todos to the local file in JSON format
    """

    STORE_TODOS.write_text(
        json.dumps([todo.model_dump() for todo in todos.values()], indent=2)+"\n"
    )


def _get_or_raise(todo_id: str)->tuple[dict[str, Todo], Todo]:
    todos=_load_todos()
    todo=todos.get(todo_id)

    if todo is None:
        raise ValueError(f"Todo with id {todo_id} not found")
    
    return todos, todo