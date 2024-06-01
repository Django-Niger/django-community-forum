API Reference
=============

Automatically generated from your module docstrings.

Hooks
-----
.. autofunction:: forum.hooks.check_user_permission

This function is a hook used by the forum application to check if a user has the permission to create discussions. By default, it returns `True`, allowing access to all users. Override this function to implement custom access control logic.
