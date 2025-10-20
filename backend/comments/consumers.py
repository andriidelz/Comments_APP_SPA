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
        

# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from channels.db import database_sync_to_async
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from django.contrib.auth.models import AnonymousUser
# from .models import Comment
# from .serializers import CommentSerializer

# class CommentConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         """
#         Підключення WebSocket з перевіркою JWT.
#         Токен передається як query param: ?token=...
#         """
#         query_string = self.scope.get('query_string', b'').decode()
#         token = None
#         if 'token=' in query_string:
#             token = query_string.split('token=')[1].split('&')[0]

#         if token:
#             try:
#                 jwt_auth = JWTAuthentication()
#                 validated_token = await database_sync_to_async(jwt_auth.get_validated_token)(token)
#                 user = await database_sync_to_async(jwt_auth.get_user)(validated_token)
#                 if user:
#                     self.scope['user'] = user
#                     await self.channel_layer.group_add("comments", self.channel_name)
#                     await self.accept()
#                     return
#             except Exception as e:
#                 print("WS JWT authentication failed:", e)

#         self.scope['user'] = AnonymousUser()
#         await self.close()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard("comments", self.channel_name)

#     async def receive(self, text_data):
#         """
#         Приймає повідомлення від клієнта і поширює його всім підключеним
#         """
#         if not self.scope['user'] or self.scope['user'].is_anonymous:
#             await self.send(text_data=json.dumps({"error": "Unauthorized"}))
#             return

#         try:
#             data = json.loads(text_data)
#             comment = await database_sync_to_async(Comment.objects.create)(
#                 user=self.scope['user'], **data
#             )
#             serializer = CommentSerializer(comment)
#             await self.channel_layer.group_send(
#                 "comments",
#                 {
#                     "type": "comment.message",
#                     "message": serializer.data
#                 }
#             )
#         except Exception as e:
#             await self.send(text_data=json.dumps({"error": str(e)}))

#     async def comment_message(self, event):
#         """
#         Обробка повідомлення групи і відправка на фронтенд
#         """
#         message = event['message']
#         await self.send(text_data=json.dumps({"message": message}))