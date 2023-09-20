# Generated by Django 4.2.4 on 2023-09-20 22:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0005_chatroom_chatroom_name_alter_chatroom_chatroom_uid_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="chatroom",
            name="number_of_participants",
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name="chatroom",
            name="chatroom_uid",
            field=models.CharField(
                default="e540509e-252e-4959-a806-691385a41519", max_length=36
            ),
        ),
        migrations.AlterField(
            model_name="chirriouser",
            name="useruid",
            field=models.CharField(
                default="4b5737a8-408e-45c7-a12c-32bfa46bcbfd", max_length=36
            ),
        ),
    ]