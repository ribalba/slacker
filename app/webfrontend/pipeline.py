from django.contrib.auth.models import User
from django.contrib.auth import login

from django_slack_oauth.models import SlackUser


def debug_oauth_request(request, api_data):
    print(api_data)
    return request, api_data


def register_user(request, api_data):

    users = User.objects.filter(username=api_data['user_id'])

    if len(users) == 0:
        user = User.objects.create_user(username=api_data['user_id'])
    else:
        user = users[0]

    slacker, _ = SlackUser.objects.get_or_create(slacker=user)
    slacker.access_token = api_data.pop('access_token')
    slacker.extras = api_data
    slacker.save()

    request.created_user = user

    login(request, user)

    return request, api_data