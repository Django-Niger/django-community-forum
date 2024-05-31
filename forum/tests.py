from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from .models import Discussion, Post
from .forms import DiscussionForm, PostForm


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


class DiscussionViewTests(TestCase):
    def test_view_discussions_list(self):
        response = self.client.get(reverse("forum:discussions_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No discussions are available.")

    def test_view_discussion_detail(self):
        discussion = Discussion.objects.create(title="Test Discussion")
        response = self.client.get(
            reverse("forum:discussion_detail", args=[discussion.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, discussion.title)


class CreateDiscussionViewTests(TestCase):
    def test_form_display(self):
        response = self.client.get(reverse("forum:create_discussion"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["form"], DiscussionForm)


class CreatePostViewTests(TestCase):
    def test_form_display(self):
        discussion = Discussion.objects.create(title="Test Discussion")
        response = self.client.get(reverse("forum:create_post", args=[discussion.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["form"], PostForm)
