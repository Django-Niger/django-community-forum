from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect, get_object_or_404
from .models import Discussion, Post
from .forms import DiscussionForm, PostForm
from .models import Discussion


def discussions_list(request):
    discussions = Discussion.objects.all()
    return render(request, "forum/discussions_list.html", {"discussions": discussions})


def discussion_detail(request, pk):
    discussion = get_object_or_404(Discussion, pk=pk)
    return render(request, "forum/discussion_detail.html", {"discussion": discussion})


def create_discussion(request):
    if request.method == "POST":
        form = DiscussionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("forum:discussions_list")
    else:
        form = DiscussionForm()
    return render(request, "forum/create_discussion.html", {"form": form})


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
