import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from chat.models import Message, ChirrioUser, ChatRoom


def save_message(room: str, email: str, text: str, time: str) -> None:
    db_author = ChirrioUser.objects.get_by_natural_key(username=email)
    db_room = ChatRoom.objects.get(chatroom_uid=room)
    db_message = Message.objects.create(chatroom_id=db_room, user_id=db_author, text=text)
    db_message.save()


class ChatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_id = None
        self.room_group_id = None

    def connect(self):
        print("Received new connection")
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_id = "chat_%s" % self.room_id

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_id, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_id, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data=None, bytes_data=None):
        print("Received new message:", text_data)
        text_data_json = json.loads(text_data)
        room = text_data_json["roomId"]
        content = text_data_json["content"]
        author = text_data_json["author"]
        time = text_data_json["timestamp"]
        save_message(room, author, content, time)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_id, {
                "type": "chat_message",
                "room_id": room,
                "content": content,
                "author": author,
                "timestamp": time
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        # Send message to WebSocket
        self.send(text_data=json.dumps(
            {"content": event["content"], "roomId": event["room_id"], "author": event["author"],
             "timestamp": event["timestamp"]})
        )
