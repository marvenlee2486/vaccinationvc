from telegram import Update
from telegram.ext import CallbackContext
from utils.constants import State

def stop_callback(update: Update, context: CallbackContext) -> None:
    """End Conversation by command."""
    update.message.reply_text('Okay, bye.')
    if(context.user_data.get("access_token")):
        del(context.user_data["access_token"])
    return State.END.value
