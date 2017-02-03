import uuid

from django.db import models

class MySlackUser(models.Model):
    slacker_id = models.CharField(max_length=20, db_index=True)
    team_id = models.CharField(max_length=20, db_index=True)
    real_name = models.CharField(max_length=500)
    image_24 = models.URLField()
    data = models.TextField()

class SlackUserOnline(models.Model):
    #refactor this to slacker and not slacker_id
    slacker_id = models.ForeignKey(MySlackUser)
    status = models.CharField(max_length=10)
    date_time = models.DateTimeField(auto_created=True, auto_now_add=True)
