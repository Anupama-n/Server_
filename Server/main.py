from fastapi import FastAPI, Depends
from login import login, read_protected
from database import get_db_vehicle, init_db
from sqlalchemy.orm import Session
from vehicles import post
import models
import schemas

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
