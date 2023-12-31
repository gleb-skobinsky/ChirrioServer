# Generated by Django 4.2.4 on 2023-11-02 18:54

from django.db import migrations, models
import django_resized.forms


class Migration(migrations.Migration):
    dependencies = [
        ("chat", "0002_alter_chatroom_chatroom_uid_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="chatroom",
            name="chatroom_uid",
            field=models.CharField(
                default="897f881c-c6ea-4b13-a24e-01cd8e58cb4a", max_length=36
            ),
        ),
        migrations.AlterField(
            model_name="chirriouser",
            name="image",
            field=django_resized.forms.ResizedImageField(
                crop=None,
                force_format=None,
                keep_meta=True,
                null=True,
                quality=-1,
                scale=None,
                size=[1000, 1000],
                upload_to="",
            ),
        ),
        migrations.AlterField(
            model_name="chirriouser",
            name="useruid",
            field=models.CharField(
                default="9cc1809b-8f84-46d5-a714-d1933ac30a61", max_length=36
            ),
        ),
    ]
