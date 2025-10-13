from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Comment
from .serializers import CommentSerializer
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
# from captcha import captcha_check
from rest_framework import status
from .forms import CommentCaptchaForm

from captcha.models import CaptchaStore
from rest_framework.decorators import api_view

@api_view(['GET'])
def generate_captcha_key(request):
    new_key = CaptchaStore.generate_key()
    return Response({'key': new_key})

class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.filter(parent=None).order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]  # JWT required

    def get_queryset(self):
        queryset = Comment.objects.filter(parent=None)
        sort_by = self.request.query_params.get('sort_by', '-created_at')
        if sort_by in ['user_name', '-user_name', 'email', '-email', 'created_at', '-created_at']:
            queryset = queryset.order_by(sort_by)
        return queryset

    @method_decorator(cache_page(60 * 5))  # Cache for 5 min
    def list(self, request, *args, **kwargs):
        page = request.query_params.get('page', 1)
        queryset = self.get_queryset()[(int(page)-1)*25:int(page)*25]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # @captcha_check('captcha')
    def create(self, request, *args, **kwargs):
        if 'file' in request.FILES:
            file = request.FILES['file']
            if file.size > 100 * 1024 or not file.name.endswith('.txt'):
                return Response({'error': 'Invalid file'}, status=status.HTTP_400_BAD_REQUEST)
            
    # Validate CAPTCHA using form
        form = CommentCaptchaForm(request.POST, request_data=request.data)
        if not form.is_valid():
            errors = {}
            if form.errors.get('captcha'):
                errors['captcha'] = [form.errors['captcha'][0]]  # Extract CAPTCHA error
            if not form.serializer.is_valid():  # Add serializer errors
                errors.update(form.serializer.errors)
            return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)
        
        # CAPTCHA and data valid; save via serializer
        serializer = form.serializer
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            
        # serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # self.perform_create(serializer)
        # return Response(serializer.data, status=status.HTTP_201_CREATED)