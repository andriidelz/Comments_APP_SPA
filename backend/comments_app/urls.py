from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# from comments.views import generate_captcha_key

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('comments.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('captcha/key/', generate_captcha_key, name='captcha-key'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# path('captcha/', include('captcha.urls')), second variant
# path('', include('comments.urls')), third variant
# path('captcha/key/', generate_captcha_key, name='captcha-key'),