import datetime

import requests
from django.core.management.base import BaseCommand, CommandError

import json
import pytz
import pprint

from app.config import SENTIMENT_KEY

pp = pprint.PrettyPrinter(indent=4)

from django_slack_oauth.models import SlackUser

from webfrontend.models import SlackChannel, SlackMessage, MySlackUser
from django.utils import timezone

class Command(BaseCommand):
    help = 'Collects all the channels from Slack'

#    def add_arguments(self, parser):
#        print (parser)

    def handle(self, *args, **options):

        for sm in SlackMessage.objects.filter(sentiment=None):


            payload = {
                'api-key': SENTIMENT_KEY,
                'text': sm.text
            }

            r = requests.post('https://api.sentigem.com/external/get-sentiment', data=payload)

            sm.sentiment=r.json()['polarity']
            sm.save()
