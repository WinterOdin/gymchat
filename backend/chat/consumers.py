# chat/consumers.py
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from .models import Message
from django.core import serializers
from django.contrib.auth import get_user_model
#async_to_sync in development 

class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        # Get last 10 messages
        messages = Messages.last_messages()
        content = {
            "messages": self.serialize_query(messages)
        }
        self.send_chat_message(content)


    def serialize_query(self, data):
        # Serialize data
        return serializers.serialize("JSON", data)


    def new_message(self, data):
        pass

    commands = {
        fetch_messages: fetch_messages,
        new_message: new_message
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
        self.commands[data['command']](self, text_data_json)


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
        # Chek if needs to be obj {"message": message }
        async_to_sync(self.send(text_data=json.dumps(message)))