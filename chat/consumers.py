import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
import re

class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        safe_room = re.sub(r"[^a-zA-Z0-9._-]", "-", self.scope["url_route"]["kwargs"]["room_name"])
        self.group_name = f"chat_{safe_room}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive_json(self, content, **kwargs):
        # Chat messages
        if content.get("type") == "chat.message":
            payload = {
                "type": "chat.broadcast",
                "message": content.get("message"),
                "user": (self.scope.get("user").username if self.scope.get("user") and not isinstance(self.scope["user"], AnonymousUser) else "Anonymous"),
            }
            await self.channel_layer.group_send(self.group_name, payload)

        # WebRTC signaling events
        elif content.get("type") in {"webrtc.offer", "webrtc.answer", "webrtc.ice"}:
            await self.channel_layer.group_send(self.group_name, content)

    async def chat_broadcast(self, event):
        await self.send_json({
            "type": "chat.message",
            "message": event.get("message"),
            "user": event.get("user", "Anonymous"),
        })

    async def webrtc_offer(self, event):
        await self.send_json(event)

    async def webrtc_answer(self, event):
        await self.send_json(event)

    async def webrtc_ice(self, event):
        await self.send_json(event)