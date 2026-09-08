import os
import subprocess
from pathlib import Path

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

app = FastAPI(title="IRIS Secure Backend")


BASE_DIR = Path("/Users/nitin/Desktop/IRIS/iris-math").resolve()
SANDBOX_DIR = (BASE_DIR / "sandbox").resolve()

ALLOWED_COMMANDS = {
    "python_version": ["python", "--version"],
    "list_files": ["ls"],
    "current_directory": ["pwd"]
}

API_KEYS = {
    os.getenv("IRIS_USER_KEY", "iris-user-key"): "user",
    os.getenv("IRIS_ADMIN_KEY", "iris-admin-key"): "admin"
}


class CommandRequest(BaseModel):
    command: str


class FileRequest(BaseModel):
    filename: str


def authenticate(api_key):
    role = API_KEYS.get(api_key)

    if role is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )

    return role


def require_admin(api_key):
    role = authenticate(api_key)

    if role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin permission required"
        )

    return role


def safe_command(command_name):
    command = ALLOWED_COMMANDS.get(command_name)

    if command is None:
        raise HTTPException(
            status_code=403,
            detail="Command not allowed"
        )

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        shell=False,
        cwd=BASE_DIR
    )

    return result.stdout.strip()


def safe_path(filename):
    requested_path = (SANDBOX_DIR / filename).resolve()

    if requested_path != SANDBOX_DIR and SANDBOX_DIR not in requested_path.parents:
        raise HTTPException(
            status_code=403,
            detail="Path outside sandbox"
        )

    return requested_path


SANDBOX_DIR.mkdir(exist_ok=True)


@app.get("/")
def root():
    return {
        "name": "IRIS",
        "status": "secure backend"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/command")
def command(
    request: CommandRequest,
    x_api_key: str = Header(...)
):
    require_admin(x_api_key)

    output = safe_command(request.command)

    return {
        "command": request.command,
        "output": output
    }


@app.post("/file")
def file(
    request: FileRequest,
    x_api_key: str = Header(...)
):
    require_admin(x_api_key)

    path = safe_path(request.filename)

    if not path.exists():
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    return {
        "filename": request.filename,
        "content": path.read_text()
    }