from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    def validate_text(self, value):
        import re
        if re.search(r'<(?!/)\w+[^>]*>(?!.*</\1>)', value):
            raise serializers.ValidationError("Invalid HTML: tags not closed.")
        return value