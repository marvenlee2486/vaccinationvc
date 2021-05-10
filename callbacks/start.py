from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from utils.constants import State


def start_callback(update:Update, context: CallbackContext) -> None:
    
    msg = "*Welcome to Covid19 Vaccine Bot*\n\n"
    msg += "Listed below are the following features you can take advantage of:\n"
    msg += "Type /stop to exit the bot"


    if context.user_data.get("access_token"):
        
        keyboard = [
            [
                InlineKeyboardButton(text="Issue Vaccine Cert", callback_data=str(State.ISSUE_VC.value)),
                InlineKeyboardButton(text="Update Organization Name", callback_data=str(State.ORG.value)),
                InlineKeyboardButton(text="Update Issuer Name", callback_data=str(State.ISSUER.value)),
            ]
        ]
    else:
        keyboard = [
            [
                InlineKeyboardButton(text="Registration", callback_data=str(State.REGISTER.value)),
                InlineKeyboardButton(text="Login", callback_data=str(State.LOGIN.value))
            ],
            [
                InlineKeyboardButton(text='Verify', callback_data=str(State.VERIFY.value))
            ]
        ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    if context.user_data.get(State.START_OVER.value):
        update.callback_query.answer()
        update.callback_query.message.reply_text(msg, parse_mode='MarkdownV2', reply_markup=reply_markup)
    else:
        update.message.reply_text(msg, parse_mode='MarkdownV2', reply_markup=reply_markup)

    context.user_data[State.START_OVER.value] = False
    return State.FEATURE_SELECTION.value
