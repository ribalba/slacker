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
                "users.list"
            )
            if user_list['ok'] != True:
                print ('Somehow we had an error in collect data with slack returning not ok')
            else:
                for user_from_slack in user_list['members']:

                        #We don't need the bot
                        if user_from_slack['id'] == 'USLACKBOT':
                            continue

                        slackuser_in_db = MySlackUser.objects.filter(slacker_id = user_from_slack['id'])

                        if len(slackuser_in_db) == 0:
                            slackuser_in_db = MySlackUser()
                        else:
                            slackuser_in_db = slackuser_in_db[0]

                        slackuser_in_db.slacker_id = user_from_slack['id']
                        slackuser_in_db.slack_user_access = slack_user
                        slackuser_in_db.team_id = user_from_slack['team_id']
                        if 'real_name' in user_from_slack and user_from_slack['real_name'] != '':
                            slackuser_in_db.real_name = user_from_slack['real_name']
                        else:
                            slackuser_in_db.real_name = user_from_slack['name']
                        slackuser_in_db.image_24 = user_from_slack['profile']['image_24']
                        slackuser_in_db.data = json.dumps(user_from_slack)
                        slackuser_in_db.save()

                        up = sc.api_call(
                            "users.getPresence",
                            user=user_from_slack['id']
                        )

                        if up['ok'] == True:
                            user_online = SlackUserOnline()
                            user_online.my_slack_user = slackuser_in_db
                            user_online.status = up['presence']
                            user_online.save()



