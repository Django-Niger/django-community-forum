import subprocess
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase, Client
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
        user = User.objects.create_user(username="testuser", password="12345")
        discussion = Discussion(title="Example Discussion", author=user)
        discussion.save()
        self.assertEqual(discussion.title, "Example Discussion")
        self.assertEqual(discussion.author, user)


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


class CreateDiscussionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.client.login(username="testuser", password="12345")

    def test_create_discussion_page_status_code(self):
        response = self.client.get(reverse("forum:create_discussion"))
        self.assertEqual(response.status_code, 200)

    def test_create_discussion_url_resolves(self):
        response = self.client.get(reverse("forum:create_discussion"))
        self.assertTemplateUsed(response, "forum/create_discussion.html")

    def test_create_discussion_post_success(self):
        response = self.client.post(
            reverse("forum:create_discussion"), {"title": "New Discussion"}
        )
        self.assertEqual(Discussion.objects.count(), 1)
        self.assertEqual(Discussion.objects.first().title, "New Discussion")
        self.assertRedirects(
            response,
            reverse("forum:discussions_list"),
        )

    def test_create_discussion_form_display(self):
        response = self.client.get(reverse("forum:create_discussion"))
        self.assertContains(response, "csrfmiddlewaretoken")


class DiscussionListTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.client.login(username="testuser", password="12345")
        Discussion.objects.create(title="Test Discussion", author=self.user)

    def test_create_discussion_button(self):
        """Vérifie que le bouton de création de discussion est présent."""
        response = self.client.get(reverse("forum:discussions_list"))
        self.assertContains(response, "Create New Discussion")
        self.assertContains(response, reverse("forum:create_discussion"))

    def test_discussions_list_shows_discussions(self):
        """Vérifie que les discussions sont affichées."""
        response = self.client.get(reverse("forum:discussions_list"))
        self.assertContains(response, "Test Discussion")

    def test_no_discussions_available(self):
        """Vérifie que le message 'No discussions are available.' s'affiche si aucune discussion n'est présente."""
        # Supprimer toutes les discussions pour ce test
        Discussion.objects.all().delete()
        response = self.client.get(reverse("forum:discussions_list"))
        self.assertContains(response, "No discussions are available.")
        self.assertNotContains(response, "<li>", html=True)


class DiscussionDetailTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.discussion = Discussion.objects.create(
            title="Test Discussion", author=self.user
        )
        self.url = reverse("forum:discussion_detail", args=[self.discussion.id])
        self.client.login(username="testuser", password="12345")

    def test_add_post_button_visible(self):
        response = self.client.get(self.url)
        self.assertContains(response, "Add Post")

    def test_add_post_button_not_visible_to_anonymous(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertNotContains(response, "Add Post")


class DiscussionDetailFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.discussion = Discussion.objects.create(
            title="Test Discussion", author=self.user
        )
        self.client = Client()
        self.url = reverse("forum:discussion_detail", args=[self.discussion.pk])

    def test_form_visible_for_authenticated_user(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(self.url)
        self.assertContains(response, "<form")  # Check for form presence
        self.assertContains(
            response, 'name="content"'
        )  # Check for specific input field

    def test_form_not_visible_for_unauthenticated_user(self):
        response = self.client.get(self.url)
        self.assertNotContains(response, "<form")

    def test_form_submission_creates_post(self):
        self.client.login(username="testuser", password="12345")
        post_data = {"content": "This is a new post in the discussion"}
        response = self.client.post(self.url, post_data)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(
            Post.objects.first().content, "This is a new post in the discussion"
        )
        self.assertRedirects(
            response, self.url
        )  # Assuming you redirect back to the discussion detail page

    def test_form_visibility_for_unauthenticated_users(self):
        response = self.client.get(self.url)
        self.assertNotContains(response, "csrfmiddlewaretoken", status_code=200)

    def test_form_visibility_for_authenticated_users(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(self.url)
        self.assertContains(response, "csrfmiddlewaretoken", status_code=200)

    def test_form_submission_by_authenticated_user_creates_post(self):
        self.client.login(username="testuser", password="12345")
        post_data = {"content": "New response"}
        response = self.client.post(self.url, post_data)
        self.assertEqual(Post.objects.count(), 1)
        self.assertRedirects(
            response, reverse("forum:discussion_detail", args=[self.discussion.id])
        )


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
            Notification.objects.first().message,
            "Your response has been added to the discussion.",
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


class NotificationResponseTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="pass1")
        self.user2 = User.objects.create_user(username="user2", password="pass2")
        self.discussion = Discussion.objects.create(
            title="Test Discussion", author=self.user1
        )
        self.post = Post.objects.create(
            discussion=self.discussion, author=self.user1, content="Initial post"
        )

    def test_notification_on_post_response(self):
        """
        Test that notifications are created when a post is responded to.
        """
        self.client.login(username="user2", password="pass2")
        self.client.post(
            reverse("forum:create_post", args=[self.discussion.id]),
            {"content": "Response to initial post"},
        )
        self.assertEqual(Notification.objects.count(), 2)
        self.assertTrue(
            Notification.objects.filter(user=self.user1).exists(),
            "Notification should be sent to the original post's author.",
        )
        self.assertTrue(
            Notification.objects.filter(user=self.user2).exists(),
            "Notification should be sent to the responder as confirmation.",
        )


class UserMentionTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="testpass")
        self.user2 = User.objects.create_user(username="user2", password="testpass")
        self.discussion = Discussion.objects.create(title="Test Discussion")

    def test_notification_on_user_mention(self):
        """
        Test that a notification is created when a user is mentioned in a post.
        """
        self.client.login(username="user1", password="testpass")
        mention_content = f"Hello @{self.user2.username}, check this out!"
        self.client.post(
            reverse("forum:create_post", args=[self.discussion.id]),
            {"content": mention_content},
        )
        # Check if a notification is created for user2
        self.assertTrue(Notification.objects.filter(user=self.user2).exists())
        # Check the content of the notification
        notification = Notification.objects.get(user=self.user2)
        self.assertIn("mentioned you", notification.message)
