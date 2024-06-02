API Reference
=============

This part of the documentation covers all the public interfaces of the Django-community-forum package. It is generated automatically from the source code, and includes details on functions, classes, and methods.

Hooks
-----
.. autofunction:: forum.hooks.check_user_permission

This function is a hook used by the forum application to check if a user has the permission to create discussions. By default, it returns `True`, allowing access to all users. Override this function to implement custom access control logic.


.. automodule:: forum.models
    :members: Discussion, Post, Notification

.. automodule:: forum.views
    :members: discussions_list, discussion_detail, create_discussion, create_post, edit_post, delete_post, read_notification
