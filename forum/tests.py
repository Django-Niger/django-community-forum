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
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")

    def test_form_display(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("forum:create_discussion"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["form"], DiscussionForm)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("forum:create_discussion"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("next=%s" % reverse("forum:create_discussion"), response.url)


class CreatePostViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.discussion = Discussion.objects.create(title="Test Discussion")

    def test_form_display(self):
        self.client.login(username="testuser", password="12345")
        discussion = Discussion.objects.create(title="Test Discussion")
        response = self.client.get(reverse("forum:create_post", args=[discussion.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["form"], PostForm)


class PostEditTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user", password="pass")
        self.other_user = User.objects.create_user(username="other", password="pass")
        self.discussion = Discussion.objects.create(title="Test Discussion")
        self.post = Post.objects.create(
            discussion=self.discussion, author=self.user, content="Original Content"
        )

    def test_edit_post_by_non_owner(self):
        self.client.login(username="other", password="pass")
        response = self.client.get(reverse("forum:edit_post", args=[self.post.id]))
        self.assertEqual(response.status_code, 403)


class PostDeleteTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='pass')
        self.other_user = User.objects.create_user(username='other', password='pass')
        self.discussion = Discussion.objects.create(title='Test Discussion')
        self.post = Post.objects.create(
            discussion=self.discussion, author=self.user, content='Original Content'
        )

    def test_delete_post_by_owner(self):
        self.client.login(username='user', password='pass')
        response = self.client.post(reverse('forum:delete_post', args=[self.post.id]))
        self.assertRedirects(response, reverse('forum:discussion_detail', args=[self.discussion.id]))
        # Check that the post is actually deleted
        with self.assertRaises(Post.DoesNotExist):
            Post.objects.get(id=self.post.id)

    def test_delete_post_by_non_owner(self):
        self.client.login(username='other', password='pass')
        response = self.client.post(reverse('forum:delete_post', args=[self.post.id]))
        self.assertEqual(response.status_code, 403)
        # Check that the post still exists
        self.assertTrue(Post.objects.filter(id=self.post.id).exists())
