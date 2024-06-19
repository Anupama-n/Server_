from fastapi import FastAPI, WebSocket
from contextlib import asynccontextmanager
from fastapi.responses import HTMLResponse
import json
from starlette.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from login import login, read_protected
from database import init_db
from vehicles import post, get
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/details")
async def render_login(request: Request):
    return templates.TemplateResponse("interface.html", {"request": request})

app.post("/login")(login)
app.get("/protected")(read_protected)
app.include_router(post.router)


def main():
    init_db()
    print("hi")

if __name__ == "__main__":
    import uvicorn
    main()
    uvicorn.run(app, host="0.0.0.0", port=8000)
