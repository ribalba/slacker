import uuid

from django.db import models
from django_slack_oauth.models import SlackUser


class MySlackUser(models.Model):
    slacker_id = models.CharField(max_length=20, db_index=True)
    slack_user_access = models.ForeignKey(SlackUser)
    team_id = models.CharField(max_length=20, db_index=True)
    real_name = models.CharField(max_length=500)
    image_24 = models.URLField()
    data = models.TextField()

class SlackUserOnline(models.Model):
    my_slack_user = models.ForeignKey(MySlackUser)
    status = models.CharField(max_length=10)
    date_time = models.DateTimeField(auto_created=True, auto_now_add=True)

class SlackChannel(models.Model):
    channel_id = models.CharField(max_length=20, db_index=True)
    team_id = models.CharField(max_length=20, db_index=True)
    slack_user_access = models.ForeignKey(SlackUser)
    name = models.CharField(max_length=500)
    data = models.TextField()

class SlackMessage(models.Model):
    channel_id = models.CharField(max_length=20, db_index=True)
    slack_user_access = models.ForeignKey(SlackUser)
    my_slack_user = models.ForeignKey(MySlackUser)
    ts = models.DateTimeField()
    ts_original = models.CharField(max_length=30)
    type = models.CharField(max_length=50)
    text = models.TextField()
    data = models.TextField()
    has_attachments = models.BooleanField(default=False)
    edited = models.BooleanField(default=False)
    is_starred = models.BooleanField(default=False)
    reactions = models.TextField(null=True, default=None)
    pinned_to = models.TextField(null=True, default=None)
