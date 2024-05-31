from django.shortcuts import render, get_object_or_404
from .models import Discussion


def discussions_list(request):
    discussions = Discussion.objects.all()
    return render(request, "forum/discussions_list.html", {"discussions": discussions})


def discussion_detail(request, pk):
    discussion = get_object_or_404(Discussion, pk=pk)
    return render(request, "forum/discussion_detail.html", {"discussion": discussion})
