from django.shortcuts import render, redirect
from .models import MessageThread


def chat_view(request, thread_id):
    thread = MessageThread.objects.get(id=thread_id)
    messages = thread.messages.order_by('timestamp')
    return render(request, 'messaging/chat.html', {'thread': thread, 'messages': messages})


def chat_list_view(request):
    threads = MessageThread.objects.filter(participants=request.user)
    return render(request, 'messaging/chat_list.html', {'threads': threads})


def new_chat_view(request):
    receiver_user = request.GET.get('receiver')
    if not MessageThread.objects.filter(participants=request.user).filter(participants=receiver_user).exists():
        thread = MessageThread.objects.create()
        thread.participants.set([request.user, receiver_user])
    else:
        thread = MessageThread.objects.filter(participants=request.user).filter(participants=receiver_user).first()
    return redirect('chat', thread_id=thread.id)
