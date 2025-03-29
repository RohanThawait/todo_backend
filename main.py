from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# Database setup
conn = sqlite3.connect("todos.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS todos (id INTEGER PRIMARY KEY, task TEXT)")
conn.commit()

class ToDo(BaseModel):
    task: str

@app.get("/tasks")
def get_tasks():
    cursor.execute("SELECT * FROM todos")
    return {"tasks": cursor.fetchall()}

@app.post("/tasks")
def add_task(todo: ToDo):
    cursor.execute("INSERT INTO todos (task) VALUES (?)", (todo.task,))
    conn.commit()
    return {"message": "Task added"}

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    cursor.execute("DELETE FROM todos WHERE id = ?", (task_id,))
    conn.commit()
    return {"message": "Task deleted"}
