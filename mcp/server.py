from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# Allow CORS for Chrome extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],  # Only allow GET requests
    allow_headers=["*"],
)

# Simple in-memory storage for commands
pending_command = None

@app.get("/command")
async def handle_command(action: str = "", price_selector: str = "", address_selector: str = ""):
    global pending_command
    
    # If parameters are provided, queue a command
    if action and price_selector and address_selector:
        pending_command = {
            "action": action,
            "selectors": {
                "price": price_selector,
                "address": address_selector
            }
        }
        return {"status": "Command queued"}
    
    # Otherwise, retrieve and clear the command
    if pending_command:
        cmd = pending_command
        pending_command = None
        return cmd
    
    raise HTTPException(status_code=404, detail="No command")

@app.post("/results")
async def store_results(results: dict):
    print("Scraped data:", results)  # Log to Render console
    return {"status": "Saved"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)