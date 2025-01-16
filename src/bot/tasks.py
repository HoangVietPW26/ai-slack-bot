from celery import shared_task
import slack
from . import utils
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@shared_task
def slack_messege_task(message, channel_id=None, user_id=None, thread_ts=None):
    logger.info("Starting task...")  # Add this to debug
    try:
        ollama_response = utils.chat_with_ollama(message)
        logger.info(f"Ollama response: {ollama_response}")  # Debug print
        
        if ollama_response is None:  # Check if Ollama failed
            logger.info("Ollama returned None")
            return None
            
        r = slack.send_message(ollama_response, channel_id, user_id, thread_ts)
        return r.status_code
    except Exception as e:
        logger.info(f"Error in task: {str(e)}")  # Debug print
        raise