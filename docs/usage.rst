Usage
=====

Detailed guide on using Django-community-forum:

- Creating discussions
- Managing posts
- Moderating content


Customizing Permissions
-----------------------
Django-community-forum allows you to customize user permissions through hooks. For instance, you can control who is allowed to create discussions by overriding the `check_user_permission` hook.

Here's how to implement custom permission logic:

.. code-block:: python

    from forum.hooks import check_user_permission

    def custom_permission_logic(user):
        # Replace the following logic with your own conditions
        return user.is_superuser  # Only superusers can create discussions

    # Overriding the default hook
    check_user_permission.override(custom_permission_logic)

Add this code to a module that is loaded during your Django app's initialization process, such as in an `apps.py` file inside a method that runs at startup.
