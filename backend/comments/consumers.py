import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Comment
from .serializers import CommentSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from channels.db import database_sync_to_async

class CommentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        token = self.scope['query_string'].decode().split('token=')[1] if 'token=' in self.scope['query_string'].decode() else None
        if token:
            try:
                user = await database_sync_to_async(JWTAuthentication().get_user)(token)
                if user:
                    self.scope['user'] = user
                    await self.channel_layer.group_add("comments", self.channel_name)
                    await self.accept()
                else:
                    await self.close()
            except Exception:
                await self.close()
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("comments", self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        comment = await database_sync_to_async(Comment.objects.create)(**text_data_json)
        serializer = CommentSerializer(comment)
        await self.channel_layer.group_send(
            "comments",
            {
                "type": "comment.message",
                "message": serializer.data
            }
        )

    async def comment_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))