import subprocess
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from .models import Discussion, Post, Notification
from .forms import DiscussionForm, PostForm


class CodeFormatTest(TestCase):
    def test_code_format(self):
        """
        Test to ensure that Python code adheres to Black's style using a specific version.
        """
        # Check Black version
        version_result = subprocess.run(
            ["black", "--version"], stdout=subprocess.PIPE, text=True
        )
        self.assertIn(
            "24.4.2",
            version_result.stdout,
            msg="Incorrect Black version. Expected 24.4.2.",
        )

        # Check code format
        format_result = subprocess.run(
            ["black", "--check", "."], stdout=subprocess.PIPE, text=True
        )
        self.assertEqual(
            format_result.returncode,
            0,
            msg="Code format issues found. Please run Black.",
        )


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
        self.user = User.objects.create_user(username="user", password="pass")
        self.other_user = User.objects.create_user(username="other", password="pass")
        self.discussion = Discussion.objects.create(title="Test Discussion")
        self.post = Post.objects.create(
            discussion=self.discussion, author=self.user, content="Original Content"
        )

    def test_delete_post_by_owner(self):
        self.client.login(username="user", password="pass")
        response = self.client.post(reverse("forum:delete_post", args=[self.post.id]))
        self.assertRedirects(
            response, reverse("forum:discussion_detail", args=[self.discussion.id])
        )
        # Check that the post is actually deleted
        with self.assertRaises(Post.DoesNotExist):
            Post.objects.get(id=self.post.id)

    def test_delete_post_by_non_owner(self):
        self.client.login(username="other", password="pass")
        response = self.client.post(reverse("forum:delete_post", args=[self.post.id]))
        self.assertEqual(response.status_code, 403)
        # Check that the post still exists
        self.assertTrue(Post.objects.filter(id=self.post.id).exists())


class NotificationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user", password="pass")
        self.discussion = Discussion.objects.create(title="Test Discussion")

    def test_notification_on_post_creation(self):
        """
        Test that a notification is created when a new post is added.
        """
        self.client.login(username="user", password="pass")
        self.client.post(
            reverse("forum:create_post", args=[self.discussion.id]),
            {"content": "Hello world"},
        )
        self.assertEqual(Notification.objects.count(), 1)
        self.assertEqual(Notification.objects.first().user, self.user)
        self.assertEqual(
            Notification.objects.first().message, "A new post has been added."
        )

    def test_notification_marked_as_read(self):
        """
        Test that a notification is marked as read when accessed.
        """
        notification = Notification.objects.create(
            user=self.user, message="New post created"
        )
        self.client.login(username="user", password="pass")
        self.client.get(reverse("forum:read_notification", args=[notification.id]))
        notification.refresh_from_db()
        self.assertTrue(notification.read)

    def test_custom_notification_logic(self):
        """
        Test that custom notification logic can be implemented.
        """
        # This test will depend on how you allow customization through hooks or settings.
        pass
