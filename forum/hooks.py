# forum/hooks.py


def check_user_permission(user):
    """
    Determine if the given user has permission to create a discussion.

    :param user: User instance to check
    :type user: django.contrib.auth.models.User
    :returns: True if the user has permission, False otherwise
    :rtype: bool
    """

    return True
