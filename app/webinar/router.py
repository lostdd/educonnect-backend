from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List, Dict
import uuid
from fastapi.responses import HTMLResponse

webinar_router = APIRouter()

# Словарь для хранения вебинаров и участников
webinars: Dict[str, List[WebSocket]] = {}


@webinar_router.post("/create_webinar/")
async def create_webinar():
    """Создание нового вебинара с уникальным ID."""
    webinar_id = str(uuid.uuid4())  
    webinars[webinar_id] = []  
    return {"webinar_id": webinar_id}


@webinar_router.websocket("/ws/{webinar_id}")
async def websocket_endpoint(webinar_id: str, websocket: WebSocket):
    """Подключение участников и ведущих к вебинару."""
    if webinar_id not in webinars:
        webinars[webinar_id] = []

    webinars[webinar_id].append(websocket)
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_json()
            message_type = data.get("type")
            if message_type in ["offer", "answer", "ice-candidate"]:
                await broadcast_message(webinar_id, data)
    except WebSocketDisconnect:
        webinars[webinar_id].remove(websocket)
    finally:
        webinars[webinar_id].remove(websocket)


async def broadcast_message(webinar_id: str, message: dict):
    """Шлет сообщение всем подключенным клиентам вебинара."""
    for connection in webinars[webinar_id]:
        await connection.send_json(message)
