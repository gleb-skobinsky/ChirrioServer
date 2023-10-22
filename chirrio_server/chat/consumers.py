import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from datetime import datetime
from django.utils import timezone

from chat.models import Message, ChirrioUser, ChatRoom

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

def fix_date_string(date: str) -> str:
    delimiter = date.rfind(".")
    left_string = date[:delimiter]
    right_string = date[delimiter:]
    if len(right_string) < 9:
        return date
    else:
        right_string = right_string[:7]
        return left_string + right_string + "Z"


def save_message(room: str, email: str, text: str, time: str) -> None:
    db_author = ChirrioUser.objects.get_by_natural_key(username=email)
    datetime_sent = datetime.strptime(time, DATETIME_FORMAT)
    datetime_sent = timezone.make_aware(datetime_sent, timezone.utc)
    db_room = ChatRoom.objects.get(chatroom_uid=room)
    db_message = Message.objects.create(chatroom_id=db_room, user_id=db_author, text=text, created_at=datetime_sent)
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
        text_data_json = json.loads(text_data)
        room = text_data_json["chatroom_id"]
        content = text_data_json["text"]
        author = text_data_json["user_id"]
        time = fix_date_string(text_data_json["created_at"])
        save_message(room, author["email"], content, time)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_id, {
                "type": "chat_message",
                "chatroom_id": room,
                "text": content,
                "user_id": author,
                "created_at": time,
                'sender_channel_name': self.channel_name
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        if self.channel_name != event.get('sender_channel_name'):
            self.send(text_data=json.dumps(
                {"text": event["text"],
                 "chatroom_id": event["chatroom_id"],
                 "user_id": event["user_id"],
                 "created_at": event["created_at"]}
            )
        )
