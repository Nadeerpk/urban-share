from django.urls import path
from .views import chat_view, chat_list_view, new_chat_view

urlpatterns = [
    path('new-chat', new_chat_view, name='new_chat'),
    path('chat/<int:thread_id>/', chat_view, name='chat'),
    path('chat/', chat_list_view, name='chat_list'),
]
