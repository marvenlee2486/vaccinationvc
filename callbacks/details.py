
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, replymarkup
from telegram.ext import CallbackContext
from telegram.ext.callbackqueryhandler import CallbackQueryHandler
from utils.constants import Authentication, State
from utils.apiService import ApiService
from utils.serializers import AuthenticationSerializer
from utils.errors import catch_error, catch_error_callback_query
from callbacks import start


class Org:

    @staticmethod
    @catch_error_callback_query
    def Org_prompt_info_callback(update:Update, context:CallbackContext):
        query = update.callback_query
        # Empty remove previous inline keyboard
        query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([]))
        print("feature: org_name")

        if context.user_data.get("org_name"):
            msg = f"You are updating organization name, type your organization name here"
        else:
            msg = f"Type your organization name"

        query.answer()
        query.message.reply_text(msg, parse_mode='MarkdownV2')

        return State.ORG_GET_INFO.value

    @staticmethod
    @catch_error
    def Org_get_info_callback(update:Update, context: CallbackContext):
        context.user_data["org_name"] = update.message.text
        print(f"Updating: {context.user_data.get('org_name')}")
        msg = f"Succesfully Updating Organization Name into *{context.user_data.get('org_name')}*"
        update.message.reply_text(msg, parse_mode='MarkdownV2')
        context.user_data[State.START_OVER.value] = False
        start.start_callback(update, context)
        return State.END.value



class Issuer:

    @staticmethod
    @catch_error_callback_query
    def Issuer_prompt_info_callback(update:Update, context:CallbackContext):
        query = update.callback_query
        # Empty remove previous inline keyboard
        query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([]))
        print("feature: Issuer_name")

        if context.user_data.get("Issuer_name"):
            msg = f"You are updating Issuer name, type your Issuer name here"
        else:
            msg = f"Type your Issuer name"

        query.answer()
        query.message.reply_text(msg, parse_mode='MarkdownV2')

        return State.ISSUER_GET_INFO.value

    @staticmethod
    @catch_error
    def Issuer_get_info_callback(update:Update, context: CallbackContext):
        context.user_data["Issuer_name"] = update.message.text
        print(f"Updating: {context.user_data.get('Issuer_name')}")
        msg = f"Succesfully Updating Issuer Name into *{context.user_data.get('Issuer_name')}*"
        
        update.message.reply_text(msg, parse_mode='MarkdownV2')
        context.user_data[State.START_OVER.value] = False
        start.start_callback(update, context)
        return State.END.value
   