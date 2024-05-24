from fastapi import FastAPI
from login import login, read_protected
from database import init_db

app = FastAPI()

app.post("/login")(login)
app.get("/protected")(read_protected)

def main():
    init_db()

if __name__ == "__main__":
    import uvicorn
    main()
    uvicorn.run(app, host="0.0.0.0", port=8000)
