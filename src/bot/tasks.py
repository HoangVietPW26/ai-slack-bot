from celery import shared_task
import slack
from . import utils, ai
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)

@shared_task
def slack_messege_task(message, channel_id=None, user_id=None, thread_ts=None):
    logger.info("Starting task...")  # Add this to debug
    try:
        # response = utils.chat_with_openai(message)
        # response = utils.chat_with_ollama(message)
        response = ai.query(message, raw=False)
        logger.info(f"Ollama response: {response}")  # Debug print
        
        if response is None:  # Check if Ollama failed
            logger.info("Ollama returned None")
            return None
            
        r = slack.send_message(response, channel_id, user_id, thread_ts)
        return r.status_code
    except Exception as e:
        logger.info(f"Error in task: {str(e)}")  # Debug print
        raise