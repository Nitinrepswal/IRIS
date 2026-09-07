import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="IRIS Backend")

DATABASE = "iris.db"


class ChatRequest(BaseModel):
    message: str


def get_connection():
    return sqlite3.connect(DATABASE)


def create_database():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT NOT NULL,
            response TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def save_conversation(message, response):
    connection = get_connection()

    connection.execute(
        "INSERT INTO conversations (message, response) VALUES (?, ?)",
        (message, response)
    )

    connection.commit()
    connection.close()


def get_conversations():
    connection = get_connection()

    rows = connection.execute(
        "SELECT id, message, response FROM conversations ORDER BY id"
    ).fetchall()

    connection.close()

    return rows


create_database()


@app.get("/")
def root():
    return {
        "name": "IRIS",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/chat")
def chat(request: ChatRequest):
    message = request.message
    response = f"IRIS received: {message}"

    save_conversation(message, response)

    return {
        "response": response
    }


@app.get("/history")
def history():
    conversations = get_conversations()

    return {
        "conversations": [
            {
                "id": row[0],
                "message": row[1],
                "response": row[2]
            }
            for row in conversations
        ]
    }