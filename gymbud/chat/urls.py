from rest_framework.routers import DefaultRouter
from django.urls import path, re_path
from . import consumers
from . import views

app_name = 'chat'
websocket_urlpatterns = [
    re_path(r'^chat_ws$', consumers.ChatConsumer.as_asgi()),
]


router = DefaultRouter()
router.register('users', views.UsersListView, basename="users_list")


urlpatterns = [
    path('messages/', views.MessagesModelList.as_view(), name='all_messages_list'),
    path('messages/<dialog_with>/', views.MessagesModelList.as_view(), name='messages_list'),
    path('dialogs/', views.DialogsModelList.as_view(), name='dialogs_list'),
    path('self/', views.ChatSelfInfoView.as_view(), name='self_info'),
    #path('upload/', views.UploadView.as_view(), name='fileupload'),
] + router.urls
