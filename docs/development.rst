Development
===========

How to contribute to the development of Django-community-forum.

Testing Hooks
-------------
The `check_user_permission` hook is tested to ensure that it properly restricts access based on the user's permissions. Here's an example of how we test the redirection behavior when a user is not logged in:

.. code-block:: python

    from django.urls import reverse
    from django.test import TestCase

    class CreateDiscussionViewTests(TestCase):
        def test_redirect_if_not_logged_in(self):
            response = self.client.get(reverse("forum:create_discussion"))
            self.assertEqual(response.status_code, 302)
            self.assertIn("next=%s" % reverse("forum:create_discussion"), response.url)

This test checks that the hook redirects a user to the login page if they are not authenticated, using the built-in `@login_required` decorator in conjunction with our `check_user_permission` hook.
