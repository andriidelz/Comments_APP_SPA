# comments/middleware.py
from urllib.parse import parse_qs
from rest_framework_simplejwt.authentication import JWTAuthentication
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser

class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = scope.get("query_string", b"").decode()
        token = parse_qs(query_string).get("token")
        print("TokenAuthMiddleware query:", query_string)
        if token:
            try:
                jwt_auth = JWTAuthentication()
                validated_token = await database_sync_to_async(jwt_auth.get_validated_token)(token[0])
                user = await database_sync_to_async(jwt_auth.get_user)(validated_token)
                print(f"Authenticated user: {user.username}")
                scope['user'] = user
            except Exception as e:
                print("JWT error:", e)
                scope['user'] = AnonymousUser()
        else:
            print("No token in query string")
            scope['user'] = AnonymousUser()
        return await super().__call__(scope, receive, send)
    
    
# from urllib.parse import parse_qs
# from channels.middleware import BaseMiddleware
# from channels.db import database_sync_to_async
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from django.contrib.auth.models import AnonymousUser

# class TokenAuthMiddleware(BaseMiddleware):
#     """
#     Custom middleware to authenticate WebSocket connections using JWT (SimpleJWT).
#     Extracts token from query string ?token=... and sets scope['user'].
#     """

#     async def __call__(self, scope, receive, send):
#         # Отримуємо токен з query string
#         query_string = scope.get("query_string", b"").decode()
#         token_list = parse_qs(query_string).get("token", None)

#         if token_list:
#             token = token_list[0]
#             try:
#                 jwt_auth = JWTAuthentication()
#                 # Перевірка токена (використовує sync-to-async)
#                 validated_token = await database_sync_to_async(jwt_auth.get_validated_token)(token)
#                 user = await database_sync_to_async(jwt_auth.get_user)(validated_token)
#                 scope['user'] = user
#             except Exception as e:
#                 print("WS JWT authentication failed:", e)
#                 scope['user'] = AnonymousUser()
#         else:
#             scope['user'] = AnonymousUser()

#         return await super().__call__(scope, receive, send)
