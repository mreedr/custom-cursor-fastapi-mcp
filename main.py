from fastapi import FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi_mcp import FastApiMCP
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()

posts: list[dict] = [
    {
        "id": 1,
        "author": "Corey Schafer",
        "title": "FastAPI is Awesome",
        "content": "This framework is really easy to use and super fast.",
        "date_posted": "April 20, 2025",
    },
    {
        "id": 2,
        "author": "Jane Doe",
        "title": "Python is Great for Web Development",
        "content": "Python is a great language for web development, and FastAPI makes it even better.",
        "date_posted": "April 21, 2025",
    },
]

class ReverseStringRequest(BaseModel):
    text: str

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
@app.get("/posts", response_class=HTMLResponse, include_in_schema=False)
def home():
    return f"<h1>{posts[0]['title']}</h1>"


@app.get("/api/posts/{post_id}")
def get_posts(post_id: int):
    post = next((post for post in posts if post["id"] == post_id), None)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {post_id} was not found")
    return post


@app.post("api/string-manip/reverse", operation_id="mcp_opperation")
def reverse_string(payload: ReverseStringRequest):
    return {"reversed": payload.text[::-1]}

@app.get("api/example-strings", operation_id="mcp_opperation")
def get_example_strings():
    return {"example_strings": ["Hello, world!", "FastAPI is awesome", "Python is great"]}

@app.exception_handler(StarletteHTTPException)
def http_exception_handler(request: Request, exc: StarletteHTTPException):
    if request.url.path.startswith("/api") or request.url.path.startswith("/mcp"):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )
    return HTMLResponse(status_code=exc.status_code, content=f"<h1>starlette http exception</h1>")

@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    if request.url.path.startswith("/api") or request.url.path.startswith("/mcp"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": exc.errors(), "body": exc.body},
        )
    return HTMLResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=f"<h1>validation error</h1>")


# Add MCP server to the FastAPI app
mcp = FastApiMCP(
    app,
    name="String Manipulation MCP",
    description="MCP server for the string manipulation API",
    include_operations=["mcp_opperation"]
    # describe_full_response_schema=True,  # Describe the full response JSON-schema instead of just a response example
    # describe_all_responses=True,  # Describe all the possible responses instead of just the success (2XX) response
)

mcp.mount()
