from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
import config

SLACK_BOT_OAUTH_TOKEN = config.env('SLACK_BOT_OAUTH_TOKEN', default=None, cast=str)
# Create your views here.

@csrf_exempt
@require_POST
def slack_event_endpoint(request):
    print(request.body, request.method)
    json_data = {}
    try:
        json_data = json.loads(request.body.decode('utf-8'))
    except Exception as e:
        print(e)
        pass

    data_type = json_data.get('type', None)
    print(data_type, json_data)
    allowed_types = ['url_verification', 'event_callback']
    if data_type == 'url_verification':
        return HttpResponse(json_data['challenge'], status=200)
    if data_type not in allowed_types:
        return HttpResponse('Not allowed', status=403)
    return HttpResponse("OK", status=200)