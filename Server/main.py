from fastapi import FastAPI, WebSocket
from contextlib import asynccontextmanager
from fastapi.responses import HTMLResponse
import json
# from .login import login, read_protected
# from .database import init_db
# from .vehicles import post, get
app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>Vehicle Application</h1>
        <form action="" onsubmit="sendMessage(event)">
            <label>Vehicle ID:</label>
            <input type="text" id="vehicle_id" autocomplete="off"/>
            <button type="submit">Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            /* var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            }; */
            var entryWS = new WebSocket("ws://localhost:8000/ws/entry/")
            function sendMessage(event) {
                var vehicleIdInput = document.getElementById("vehicle_id")
                entryWS.send(JSON.stringify({vehicle_id: vehicleIdInput.value}))
                vehicleIdInput.value = ''
                event.preventDefault()
            }
            entryWS.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
        </script>
    </body>
</html>
"""

@app.get("/")
async def get():
    return HTMLResponse(html)

@app.websocket("/ws/entry/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(json.dumps(data))

@app.websocket("/ws/exit/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(json.dumps(data))

# app.post("/login")(login)
# app.get("/protected")(read_protected)
# app.include_router(post.router)


def main():
    # init_db()
    print("hi")

if __name__ == "__main__":
    import uvicorn
    main()
    uvicorn.run(app, host="0.0.0.0", port=8000)
