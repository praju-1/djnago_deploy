from django.urls import path
from . import views

urlpatterns = [
    path('', views.feed_view, name='feed'),
    path('delete/<int:message_id>/', views.delete_message, name='delete_message'),
    path('comment/<int:message_id>/', views.add_comment, name='add_comment'),
    path('like_message/<int:message_id>/', views.like_message, name='like_message'),
    path('like_comment/<int:comment_id>/', views.like_comment, name='like_comment'),
]
