# forum/hooks.py


def check_user_permission(user):
    """By default, returns True to allow access if no specific hook is defined."""
    return True
