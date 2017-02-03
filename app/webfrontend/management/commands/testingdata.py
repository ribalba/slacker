from django.core.management.base import BaseCommand, CommandError

import json

from django_slack_oauth.models import SlackUser

from webfrontend.models import MySlackUser, SlackUserOnline


class Command(BaseCommand):
    help = 'Collects all the stats from Slack'

#    def add_arguments(self, parser):
#        print (parser)

    def handle(self, *args, **options):

        for slack_user in SlackUser.objects.all():
            from slackclient import SlackClient

            slack_token = slack_user.access_token
            sc = SlackClient(slack_token)
            user_list = sc.api_call(
                "channels.history",
            #    "channels.list"
                channel= 'C2F7ZR06L'
            )
            print (user_list)

