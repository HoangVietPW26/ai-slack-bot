from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
import config
import requests
from pprint import pprint
from .tasks import slack_messege_task

SLACK_BOT_OAUTH_TOKEN = config.env('SLACK_BOT_OAUTH_TOKEN', default=None, cast=str)
# Create your views here.


@csrf_exempt
@require_POST
def slack_event_endpoint(request):

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
        # pprint(event_data)
        user_id = event_data.get('user', None)
        channel_id = event_data.get('channel', None)
        
        try:
            messesage_text = event_data.get('blocks')[0].get('elements')[0].get('elements')[1].get('text')
        except Exception as e:
            print(e)
            messesage_text = event_data.get('text', None)
        
        msg_ts = event_data.get('ts', None)
        thread_ts = event_data.get('thread_ts', None) or msg_ts

        # r = slack.send_message(messesage_text, channel_id, user_id, thread_ts)
        # slack_messege_task.delay("Working...", channel_id=channel_id, user_id=user_id, thread_ts=thread_ts)
        # slack_messege_task.delay(messesage_text, channel_id=channel_id, user_id=user_id, thread_ts=thread_ts)
        slack_messege_task.apply_async(kwargs={
                "message": f"{messesage_text}", 
                "channel_id": channel_id,
                "user_id": user_id,
                'thread_ts': thread_ts
                }, countdown=0)

        return HttpResponse('OK', status=200)
    
    if data_type not in allowed_types:
        return HttpResponse('Not allowed', status=403)
    return HttpResponse("OK", status=200)