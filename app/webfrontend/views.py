import json
import operator

from datetime import datetime, timedelta

from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django_slack_oauth.models import SlackUser

from webfrontend.models import MySlackUser, SlackUserOnline,SlackMessage,SlackChannel


def logout(request):
    auth_logout(request)
    return redirect('/')


def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('main/')

    return render(request, 'login.html')

def check_team_auth(team_id, request):
    su = get_object_or_404(SlackUser, slacker=request.user)
    if su.extras['team_id'] != team_id:
        raise Http404('Team id not found with your user')


@login_required
def main(request):

    request_user_slack = SlackUser.objects.get(slacker=request.user)

    team_slack_users = MySlackUser.objects.filter(team_id = request_user_slack.extras['team_id'])

    return render(request, 'main.html', {
        'team_slack_users': team_slack_users
    })

@login_required
def details(request, team_hash, user_hash):

    check_team_auth(team_hash, request)

    my_slack_user = get_object_or_404( MySlackUser, team_id = team_hash, slacker_id = user_hash)

    my_slack_user.data = json.dumps(json.loads(my_slack_user.data), indent=4)

    stats = SlackUserOnline.objects.filter(my_slack_user=my_slack_user).order_by("date_time")

    stats_list = []

    for s in stats:
        if s.status == "active":
            stats_list.append("[new Date(\"" + str(s.date_time) + "\"), 1], ")
        else:
            stats_list.append("[new Date(\"" + str(s.date_time) + "\"), 0], ")


    online_last_month = SlackUserOnline.objects.filter(my_slack_user=my_slack_user, status="active", date_time__gte=datetime.now()-timedelta(days=30)).count()/6
    online_last_week = SlackUserOnline.objects.filter(my_slack_user=my_slack_user, status="active", date_time__gte=datetime.now()-timedelta(days=7)).count()/6



    #Find all the channels the user posts to
    slack_messages = SlackMessage.objects.filter(my_slack_user=my_slack_user)

    wordcount={}
    channelcount = {}
    sentimentcounter = {}

    for sm in slack_messages:

        for word in sm.text.split():
            if word not in wordcount:
                wordcount[word] = 1
            else:
                wordcount[word] += 1

        if sm.channel_id not in channelcount:
            channelcount[sm.channel_id] = 1
        else:
            channelcount[sm.channel_id] += 1

        if sm.sentiment not in sentimentcounter:
            sentimentcounter[sm.sentiment] = 1
        else:
            sentimentcounter[sm.sentiment] += 1


    #Format the chanel names
    channelNames = []
    for k in channelcount:
        sc = SlackChannel.objects.get(channel_id= k )
        channelNames.append("['" + sc.name + "', " + str(channelcount[k]) +"], ")

    sorted_x = sorted(wordcount.items(), key=operator.itemgetter(1))[-10:]

    return render(request, 'userdeatails.html', {
        'my_slack_user': my_slack_user,
        'stats_list': stats_list,
        'wordcount': sorted_x,
        'channelNames':channelNames,
        'sentimentcounter':sentimentcounter,
        'online_last_month':online_last_month,
        'online_last_week':online_last_week
    })
