from django.test import TestCase
from .models import Discussion


class DiscussionModelTests(TestCase):
    def test_creating_discussion(self):
        """Tests that we can create and save a Discussion."""
        discussion = Discussion(title="Example Discussion")
        discussion.save()
        self.assertEqual(discussion.title, "Example Discussion")
