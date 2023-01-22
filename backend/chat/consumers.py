# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from .models import Message
from django.core import serializers
from django.contrib.auth import get_user_model
#async_to_sync in development 
from django.shortcuts import get_object_or_404
User = get_user_model()

class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        # Get last 10 messages
        messages = Message.last_messages()
        content = {
            "messages": self.serialize_query(messages)
        }
        self.send_chat_message(content)


    def serialize_query(self, data):
        # Serialize data
        return serializers.serialize("JSON", data)


    def new_message(self, data):
        from_who = data['from_id']
        user = get_object_or_404(User, pk=from_who)
        new_message_content = Message.objects.create(
            author = user.author,
            content = data["message"]
        )
        content = {
            "command": "new_message",
            "message": self.serialize_query(new_message_content)
        }
        return self.send_chat_message(content)

    commands = {
        "fetch_messages": fetch_messages,
        "new_message": new_message
    }


    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add(self.room_group_name, self.channel_name))

        async_to_sync(self.accept())


    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard(self.room_group_name, self.channel_name))

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
    
        self.commands[text_data_json['command']](self, text_data_json)


    def send_chat_message(self, message):
        
        async_to_sync(self.channel_layer.group_send(
            self.room_group_name, {
                "type": "chat_message",
                "message": message
            }
        ))


    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
    
        async_to_sync(self.send(text_data=json.dumps(
            {
                "message": message
            }
        )))