from django.contrib import admin

from chat.models import (
    ChirrioUser,
    ChatRoom,
    Message,
    ChatRoomParticipant
)


class UserAdmin(admin.ModelAdmin):
    list_display = ["email", "first_name", "last_name", "is_staff", "is_active"]


class ChatRoomAdmin(admin.ModelAdmin):
    list_display = [
        "chatroom_uid",
        "chatroom_name",
        "last_message",
        "last_sent_user_id",
    ]


class MessageAdmin(admin.ModelAdmin):
    list_display = [
        "chatroom_id",
        "user_id",
        "text",
        "created_at"
    ]


class ChatRoomParticipantAdmin(admin.ModelAdmin):
    list_display = ["user_id", "chatroom_id"]


admin.site.register(ChirrioUser, UserAdmin)
admin.site.register(ChatRoom, ChatRoomAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(ChatRoomParticipant, ChatRoomParticipantAdmin)
