import datetime

from django.core.management.base import BaseCommand, CommandError

import json
import pytz
import pprint
pp = pprint.PrettyPrinter(indent=4)

from django_slack_oauth.models import SlackUser

from webfrontend.models import SlackChannel, SlackMessage, MySlackUser
from django.utils import timezone

class Command(BaseCommand):
    help = 'Collects all the channels from Slack'

#    def add_arguments(self, parser):
#        print (parser)

    def handle(self, *args, **options):

        for slack_user in SlackUser.objects.all():
            from slackclient import SlackClient

            slack_token = slack_user.access_token
            sc = SlackClient(slack_token)
            channel_list = sc.api_call(
                "channels.list"
            )

            if channel_list['ok'] != True:
                print('Somehow we had an error in collect data with slack returning not ok')
            else:
                for channel_from_slack in channel_list['channels']:
                    channel_in_db = SlackChannel.objects.filter(channel_id=channel_from_slack['id'])

                    if len(channel_in_db) == 0:
                        channel_in_db = SlackChannel()
                    else:
                        channel_in_db = channel_in_db[0]

                    channel_in_db.channel_id = channel_from_slack['id']
                    channel_in_db.team_id = slack_user.extras['team_id']
                    channel_in_db.slacker_id = slack_user
                    channel_in_db.name = channel_from_slack['name']
                    channel_in_db.data = json.dumps(channel_from_slack)
                    channel_in_db.save()


                    messages = []

                    channel_data = sc.api_call(
                        "channels.history",
                        channel = channel_from_slack['id'],
                        count = 2
                    )

                    messages += channel_data['messages']

                    while channel_data['has_more'] == True:
                        channel_data = sc.api_call(
                            "channels.history",
                            channel=channel_from_slack['id'],
                            count=100,
                            latest= channel_data['messages'][len(channel_data['messages'])-1]['ts']
                        )

                        messages += channel_data['messages']


                    #Now we loop through all the messages
                    for m in messages:
                        ts= datetime.datetime.fromtimestamp(float(m['ts']), tz=pytz.UTC)
                        slack_message_already_in_db = SlackMessage.objects.filter(channel_id = channel_from_slack['id'], ts = ts).count()

                        if slack_message_already_in_db == 0:
                            slack_message_in_db = SlackMessage()
                            slack_message_in_db.channel_id = channel_from_slack['id']
                            slack_message_in_db.slack_user_access = slack_user
                            slack_message_in_db.my_slack_user = MySlackUser.objects.get(slacker_id=m['user'])
                            slack_message_in_db.ts = ts
                            slack_message_in_db.ts_original = m['ts']
                            slack_message_in_db.type = m['type']
                            slack_message_in_db.text = m['text']
                            slack_message_in_db.data = json.dumps(m)
                            slack_message_in_db.has_attachments = 'attachments' in m
                            slack_message_in_db.edited = 'edited' in m
                            slack_message_in_db.is_starred
                            slack_message_in_db.reactions = json.dumps(m['reactions']) if ('reactions' in m) else None
                            slack_message_in_db.pinned_to = json.dumps(m['pinned_to']) if ('pinned_to' in m) else None

                            slack_message_in_db.save()
