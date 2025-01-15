from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
import config
import requests
from pprint import pprint

SLACK_BOT_OAUTH_TOKEN = config.env('SLACK_BOT_OAUTH_TOKEN', default=None, cast=str)
# Create your views here.

def send_message(message, channel_id=None, user_id=None):
    url =  "https://slack.com/api/chat.postMessage"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {SLACK_BOT_OAUTH_TOKEN}",
        "Accept": "application/json"
    }
    if user_id:
        message = f"<@{user_id}> {message}"
    data = {
        "channel": f"{channel_id}",
        "text": f"{message}".strip()
    }
    return requests.post(url, headers=headers, json=data)


@csrf_exempt
@require_POST
def slack_event_endpoint(request):
    # print(request.body, request.method)
    json_data = {}
    try:
        json_data = json.loads(request.body.decode('utf-8'))
    except Exception as e:
        print(e)
        pass

    data_type = json_data.get('type', None)
    # print(data_type, json_data, json_data.keys())

    allowed_types = ['url_verification', 'event_callback']

    if data_type == 'url_verification':
        return HttpResponse(json_data['challenge'], status=200)
    elif data_type == 'event_callback':
        event_data = json_data.get('event', {})
        pprint(event_data)
        user_id = event_data.get('user', None)
        channel_id = event_data.get('channel', None)
        
        try:
            messesage_text = event_data.get('blocks')[0].get('elements')[0].get('elements')[1].get('text')
        except Exception as e:
            print(e)
            messesage_text = event_data.get('text', None)
        r = send_message(messesage_text, channel_id, user_id)
        print(r.json())
        return HttpResponse('OK', status=r.status_code)
    
    if data_type not in allowed_types:
        return HttpResponse('Not allowed', status=403)
    return HttpResponse("OK", status=200)