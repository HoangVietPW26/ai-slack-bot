import config
import requests


SLACK_BOT_OAUTH_TOKEN = config.env('SLACK_BOT_OAUTH_TOKEN', default=None, cast=str)


def send_message(message, channel_id=None, user_id=None, thread_ts=None):
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

    if thread_ts:
        data['thread_ts'] = thread_ts
    print("****")
    print(data)

    return requests.post(url, headers=headers, json=data)