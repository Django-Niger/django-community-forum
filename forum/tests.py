from django.contrib.auth.models import User
from django.test import TestCase
from .models import Discussion, Post


class DiscussionModelTests(TestCase):
    def test_creating_discussion(self):
        """Tests that we can create and save a Discussion."""
        discussion = Discussion(title="Example Discussion")
        discussion.save()
        self.assertEqual(discussion.title, "Example Discussion")


class PostModelTests(TestCase):
    def test_creating_post(self):
        user = User.objects.create_user(username="testuser", password="12345")
        discussion = Discussion.objects.create(title="Test Discussion")
        post = Post.objects.create(
            discussion=discussion, author=user, content="Test content"
        )
        post.save()
        self.assertEqual(post.discussion, discussion)
        self.assertEqual(post.author, user)
        self.assertEqual(post.content, "Test content")
