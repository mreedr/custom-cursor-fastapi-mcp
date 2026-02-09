from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel
from fastapi_mcp import FastApiMCP
from starlette.exceptions import HTTPException

from auth.jwt import create_access_token, get_current_user

app = FastAPI(title="String Manipulation API")

class ReverseStringRequest(BaseModel):
    text: str

class LoginRequest(BaseModel):
    username: str
    password: str

def is_admin_user_password(password: str) -> bool:
    return password == "my_secret_password"

@app.post("/login", operation_id="login")
def login(payload: LoginRequest):
    if payload.username != "admin" or not is_admin_user_password(payload.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    token = create_access_token(payload.username)
    return {"access_token": token, "token_type": "bearer"}

@app.post("/api/string-manip/reverse", operation_id="reverse_given_string")
def reverse_string(
    payload: ReverseStringRequest,
    user: str = Depends(get_current_user),
):
    return {"reversed": payload.text[::-1]}

@app.get("/api/example-strings", operation_id="example_string")
async def get_example_strings(user: str = Depends(get_current_user)):
    return {"example_strings": ["Hello, world!", "FastAPI is awesome", "Python is great"]}

mcp = FastApiMCP(
    app,
    name="String Manipulation MCP",
    description="MCP server for the string manipulation API",
    include_operations=["login", "example_string", "reverse_given_string"]
)

mcp.mount()

