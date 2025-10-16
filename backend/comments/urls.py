from django.urls import path
from .views import CommentListCreateView, generate_captcha_key
from captcha.views import captcha_image

urlpatterns = [
    path('comments/', CommentListCreateView.as_view(), name='comments'),
    path('captcha/key/', generate_captcha_key, name='captcha-key'),
    path('captcha/image/<str:key>/', captcha_image, name='captcha-image'),
]