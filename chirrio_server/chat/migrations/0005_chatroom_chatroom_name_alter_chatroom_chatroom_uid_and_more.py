# Generated by Django 4.2.4 on 2023-09-19 21:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0004_alter_chatroom_chatroom_uid_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="chatroom",
            name="chatroom_name",
            field=models.CharField(default="", max_length=1024),
        ),
        migrations.AlterField(
            model_name="chatroom",
            name="chatroom_uid",
            field=models.CharField(
                default="c39a1094-d64d-4fad-a74e-ba5fb6451d69", max_length=36
            ),
        ),
        migrations.AlterField(
            model_name="chirriouser",
            name="useruid",
            field=models.CharField(
                default="2e0e9dd4-f1a0-4cd6-a6bc-9d983ab403f9", max_length=36
            ),
        ),
    ]
