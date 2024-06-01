# forum/hooks.py


def check_user_permission(user):
    """Par défaut, retourne True pour permettre l'accès si aucun hook spécifique n'est défini."""
    return True
