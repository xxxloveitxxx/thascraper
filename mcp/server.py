from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# Allow CORS for Chrome extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict to your domain later
    allow_methods=["*"],
    allow_headers=["*"],
)

active_connections = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            await websocket.receive_text()  # Keep connection alive
    except WebSocketDisconnect:
        active_connections.remove(websocket)

@app.post("/command")
async def send_command(command: dict):
    for connection in active_connections:
        await connection.send_json(command)
    return {"status": "Command sent"}

@app.post("/results")
async def store_results(results: dict):
    print("Scraped data:", results)  # Forward to Hermes later
    return {"status": "Saved"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)  # Render uses port 10000