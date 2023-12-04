from fastapi import FastAPI,WebSocket,Request
from fastapi.responses import HTMLResponse
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from api_test import fetch_data
import asyncio
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

#@app.get("/", response_class=HTMLResponse)
#async def get(request: Request):
#    return templates.TemplateResponse("index_socket.html",{"request": request})



@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = fetch_data()  # Fetch data from Cosmos Mongodb
        await websocket.send_json(data)
        await asyncio.sleep(1)  # Add a delay to prevent overwhelming the client




if __name__ == "__socket_test__":
  uvicorn.run(app, host="0.0.0.0", port=8001)