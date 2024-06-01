from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .hooks import check_user_permission
from django.http import HttpResponseForbidden
from .models import Discussion, Post
from .forms import DiscussionForm, PostForm
from .models import Discussion


def discussions_list(request):
    discussions = Discussion.objects.all()
    return render(request, "forum/discussions_list.html", {"discussions": discussions})


def discussion_detail(request, pk):
    discussion = get_object_or_404(Discussion, pk=pk)
    return render(request, "forum/discussion_detail.html", {"discussion": discussion})


@login_required
def create_discussion(request):
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
    post = get_object_or_404(Post, pk=pk)
    if post.author != request.user:
        return HttpResponseForbidden("You are not allowed to delete this post")

    if request.method == "POST":
        discussion_id = post.discussion.pk
        post.delete()
        return redirect("forum:discussion_detail", pk=discussion_id)

    return render(request, "forum/delete_post.html", {"post": post})
