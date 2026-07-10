from django.urls import path

from . import views

app_name = 'learning_logs'
urlpatterns = [
    path('', views.index, name='index'),
    path('topics/', views.topics, name='topics'),
    path('topics/<int:topic_id>/', views.topic, name='topic'),
    path('new_topic/', views.new_topic, name='new_topic'),
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    path('topic/<int:topic_id>/add_member/', views.add_member, name='add_member'),
    path('topic/<int:topic_id>/remove_member/<int:member_id>/',views.remove_member,name='remove_member'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('add_comment/<int:entry_id>/',views.add_comment,name='add_comment'),
    path('notifications/',views.notifications,name='notifications'),
    path('entry/<int:entry_id>/',views.entry_detail,name='entry_detail'),
]