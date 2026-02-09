import os
import secrets

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel
from fastapi_mcp import FastApiMCP

from auth.jwt import create_access_token, get_current_user

app = FastAPI(title="String Manipulation API")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "my_secret_password")

class ReverseStringRequest(BaseModel):
    text: str

class LoginRequest(BaseModel):
    username: str
    password: str


@app.post("/login", operation_id="login")
def login(payload: LoginRequest):
    if payload.username != "admin" or payload.password != ADMIN_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    token = create_access_token(payload.username)
    return {"access_token": token, "token_type": "bearer"}


@app.post("/api/string-manip/reverse", operation_id="reverse_given_string")
def reverse_string(
    payload: ReverseStringRequest,
):
    return {"reversed": payload.text[::-1]}


@app.get("/api/example-strings", operation_id="example_string")
def get_example_strings(user: str = Depends(get_current_user)):
    return {"example_strings": ["Hello, world!", "FastAPI is awesome", "Python is great"]}


@app.get("/api/crypto/ethereum/address", operation_id="random_eth_address")
def random_eth_address():
    return {"address": f"0x{secrets.token_hex(20)}"}


mcp = FastApiMCP(
    app,
    name="String Manipulation MCP",
    description="MCP server for the string manipulation API",
    include_operations=[
        "login",
        "example_string",
        "reverse_given_string",
        "random_eth_address",
    ]
)


mcp.mount()

