from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .hooks import check_user_permission
from django.http import HttpResponseForbidden
from .models import Discussion, Post
from .forms import DiscussionForm, PostForm
from .models import Discussion


def discussions_list(request):
    """
    Display a list of all discussions.

    :param request: HttpRequest object
    :return: HttpResponse object with the list of discussions
    """
    discussions = Discussion.objects.all()
    return render(request, "forum/discussions_list.html", {"discussions": discussions})


def discussion_detail(request, pk):
    """
    Display the details of a specific discussion.

    :param request: HttpRequest object
    :param pk: Primary key of the discussion to display
    :return: HttpResponse object with discussion details
    """
    discussion = get_object_or_404(Discussion, pk=pk)
    return render(request, "forum/discussion_detail.html", {"discussion": discussion})


@login_required
def create_discussion(request):
    """
    Create a new discussion if the user has the permission.

    :param request: HttpRequest object
    :return: HttpResponse object; redirects to the discussion list or displays the form
    """
    if not check_user_permission(request.user):
        return HttpResponseForbidden("You are not authorized to create a discussion.")

    if request.method == "POST":
        form = DiscussionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("forum:discussions_list")
    else:
        form = DiscussionForm()
    return render(request, "forum/create_discussion.html", {"form": form})


@login_required
def create_post(request, pk):
    """
    Create a new post in a specific discussion.

    :param request: HttpRequest object
    :param pk: Primary key of the discussion in which to create the post
    :return: HttpResponse object; redirects to the discussion detail or displays the form
    """
    discussion = get_object_or_404(Discussion, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.discussion = discussion
            post.author = request.user
            post.save()
            return redirect("forum:discussion_detail", pk=discussion.pk)
    else:
        form = PostForm()
    return render(
        request, "forum/create_post.html", {"form": form, "discussion": discussion}
    )


@login_required
def edit_post(request, pk):
    """
    Allows the user to edit an existing post if they are the author.

    Checks if the user is the author of the post; if not, a forbidden response is returned.
    If the user is the author and the form is submitted and valid, the post is updated.

    :param request: HttpRequest object
    :param pk: Primary key of the post to be edited
    :return: HttpResponse object; redirects to the discussion detail or displays the form for editing
    """
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return HttpResponseForbidden("You are not allowed to edit this post")

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("forum:discussion_detail", pk=post.discussion.pk)
    else:
        form = PostForm(instance=post)

    return render(request, "forum/edit_post.html", {"form": form, "post": post})


@login_required
def delete_post(request, pk):
    """
    Allows the user to delete their own post.

    Validates that the logged-in user is the author of the post. If not, a forbidden response is given.
    If the user is the author, the post is deleted upon confirmation.

    :param request: HttpRequest object
    :param pk: Primary key of the post to be deleted
    :return: HttpResponse object; redirects to the discussion detail if deletion is successful
    """
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return HttpResponseForbidden("You are not allowed to delete this post")

    if request.method == "POST":
        discussion_id = post.discussion.pk
        post.delete()
        return redirect("forum:discussion_detail", pk=discussion_id)

    return render(request, "forum/delete_post.html", {"post": post})
