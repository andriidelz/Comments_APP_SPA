from django.test import TestCase
from .models import Comment

class CommentTestCase(TestCase):
    def test_comment_creation(self):
        comment = Comment.objects.create(user_name='Test', email='test@example.com', text='Hello')
        self.assertEqual(comment.user_name, 'Test')