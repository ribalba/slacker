import json

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django_slack_oauth.models import SlackUser

from webfrontend.models import MySlackUser, SlackUserOnline


def logout(request):
    auth_logout(request)
    return redirect('/')


def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('main/')

    return render(request, 'login.html')

@login_required
def main(request):
    request_user_slack = SlackUser.objects.get(slacker=request.user)

    team_slack_users = MySlackUser.objects.filter(team_id = request_user_slack.extras['team_id'])

    return render(request, 'main.html', {
        'team_slack_users': team_slack_users
    })

@login_required
def details(request, team_hash, user_hash):

    my_slack_user = get_object_or_404( MySlackUser, team_id = team_hash, slacker_id = user_hash)

    my_slack_user.data = json.dumps(json.loads(my_slack_user.data), indent=4)

    stats = SlackUserOnline.objects.filter(slacker_id=my_slack_user).order_by("date_time")

    stats_list = []

    for s in stats:
        if s.status == "active":
            stats_list.append("[new Date(\"" + str(s.date_time) + "\"), 1], ")
        else:
            stats_list.append("[new Date(\"" + str(s.date_time) + "\"), 0], ")



    return render(request, 'userdeatails.html', {
        'my_slack_user': my_slack_user,
        'stats_list': stats_list,
    })
