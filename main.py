from fastapi import FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi_mcp import FastApiMCP
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI(title="String Manipulation API")

class ReverseStringRequest(BaseModel):
    text: str

@app.post("/api/string-manip/reverse", operation_id="reverse_given_string")
def reverse_string(payload: ReverseStringRequest):
    return {"reversed": payload.text[::-1]}

@app.get("/api/example-strings", operation_id="example_string")
async def get_example_strings():
    return {"example_strings": ["Hello, world!", "FastAPI is awesome", "Python is great"]}

mcp = FastApiMCP(
    app,
    name="String Manipulation MCP",
    description="MCP server for the string manipulation API",
    include_operations=["example_string", "reverse_given_string"]
)

mcp.mount()

