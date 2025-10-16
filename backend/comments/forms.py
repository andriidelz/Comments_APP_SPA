from django import forms
from captcha.fields import CaptchaField
from .serializers import CommentSerializer  

class CommentCaptchaForm(forms.Form):
    captcha = CaptchaField()

    def __init__(self, *args, **kwargs):
        self.serializer = None
        self.request_data = kwargs.pop('request_data', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if self.request_data:
            self.serializer = CommentSerializer(data=self.request_data)
            if not self.serializer.is_valid():
                raise forms.ValidationError("Invalid comment data")
        return cleaned_data