from fastapi import FastAPI
from contextlib import asynccontextmanager
from login import login, read_protected
from database import init_db
from vehicles import post, get

app = FastAPI()

app.post("/login")(login)
app.get("/protected")(read_protected)
app.include_router(post.router)


def main():
    init_db()

if __name__ == "__main__":
    import uvicorn
    main()
    uvicorn.run(app, host="0.0.0.0", port=8000)
