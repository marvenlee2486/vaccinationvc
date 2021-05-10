from telegram import Update
from telegram.ext import CallbackContext
from utils.constants import State
from callbacks import start
def stop_callback(update: Update, context: CallbackContext) -> None:
    """End Conversation by command."""
    update.message.reply_text('Okay, bye.')
    if(context.user_data.get("access_token")):
        del(context.user_data["access_token"])
    return State.END.value

def stop_callback_second_level(update: Update, context: CallbackContext):
    context.user_data[State.START_OVER.value] = False
    start.start_callback(update, context)
    return State.END.value