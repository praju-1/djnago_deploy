from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Message, Comment, Like

@login_required
def feed_view(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            Message.objects.create(user=request.user, text=text)
            return redirect('/feed/')
    
    messages_list = Message.objects.all().order_by('-created_at')
    return render(request, 'feed/feed.html', {'messages': messages_list})

@login_required
def delete_message(request, message_id):
    try:
        message = Message.objects.get(id=message_id, user=request.user)
        message.delete()
        messages.success(request, "Message deleted successfully!")
    except Message.DoesNotExist:
        messages.error(request, "Message not found or you do not have permission to delete this.")
    return redirect('/feed/')

@login_required
def add_comment(request, message_id):
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            message = Message.objects.get(id=message_id)
            Comment.objects.create(message=message, user=request.user, text=text)
            messages.success(request, "Comment added successfully!")
        else:
            messages.error(request, "Comment cannot be empty.")
    return redirect('/feed/')

@login_required
def like_message(request, message_id):
    try:
        message = Message.objects.get(id=message_id)
        # Check if the user has already liked this message
        if Like.objects.filter(user=request.user, message=message).exists():
            messages.error(request, "You already liked this message.")
        else:
            Like.objects.create(user=request.user, message=message)
            messages.success(request, "Message liked successfully!")
    except Message.DoesNotExist:
        messages.error(request, "Message not found.")
    return redirect('/feed/')

@login_required
def like_comment(request, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
        # Check if the user has already liked this comment
        if Like.objects.filter(user=request.user, comment=comment).exists():
            messages.error(request, "You already liked this comment.")
        else:
            Like.objects.create(user=request.user, comment=comment)
            messages.success(request, "Comment liked successfully!")
    except Comment.DoesNotExist:
        messages.error(request, "Comment not found.")
    return redirect('/feed/')
