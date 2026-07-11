from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# Allow CORS for Chrome extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

pending_command = None

@app.post("/command")
async def send_command(command: dict):
    global pending_command
    pending_command = command
    return {"status": "Command queued"}

@app.get("/command")
async def get_command():
    global pending_command
    if pending_command:
        cmd = pending_command
        pending_command = None
        return cmd
    raise HTTPException(status_code=404, detail="No command")

@app.post("/results")
async def store_results(results: dict):
    print("Scraped data:", results)  # Forward to Hermes later
    return {"status": "Saved"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)