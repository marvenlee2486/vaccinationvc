from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, replymarkup
from telegram.ext import CallbackContext
from telegram.ext.callbackqueryhandler import CallbackQueryHandler
from utils.constants import Authentication, State
from utils.apiService import ApiService
from utils.serializers import AuthenticationSerializer
from utils.errors import catch_error, catch_error_callback_query
from callbacks import start, details


class Verify:

    @staticmethod
    @catch_error_callback_query
    def verify_prompt_info_callback(update:Update, context:CallbackContext):
        query = update.callback_query
        # Empty remove previous inline keyboard
        query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([]))
        
    
        msg = "Enter the the certification URL"
       
        query.answer()
        query.message.reply_text(msg, parse_mode='MarkdownV2')
        return State.VERIFY_GET_INFO.value


    @staticmethod
    @catch_error
    def verify_get_info_callback(update:Update, context: CallbackContext):

        
        context.user_data["URL"] = update.message.text
        print(f"Updating: {context.user_data.get('URL')}")

        context.user_data[State.START_OVER.value] = True
        Verify.verify_submit_info_callback(update, context)
        return State.END.value 

    @staticmethod
    @catch_error_callback_query
    def verify_submit_info_callback(update: Update, context: CallbackContext):
        query = update.callback_query
        URL = context.user_data["URL"]
        print("Verifying")
        if (ApiService.verifying_credential(sharing_url= URL, context = context)):

            print("Suceess")
            msg = "The ceritification is correct\. Returning to main menu\.\.\.\."
            del context.user_data["URL"]
            img ="https://previews.123rf.com/images/boykung/boykung1108/boykung110800168/10388753-yes-symbol-green-color-gradient-white-background.jpg"
            update.message.reply_text(msg, parse_mode='MarkdownV2')
            update.message.reply_photo(photo=img)
            context.user_data[State.START_OVER.value] = False
            start.start_callback(update, context)
            return State.END.value
        
        else:
            print("Failed")
            msg = "The ceritification is Wrong\. Returning to main menu\.\.\.\."
            del context.user_data["URL"]
            img = "http://www.clipartbest.com/cliparts/RTd/L4X/RTdL4X9Ec.png"
            update.message.reply_text(msg, parse_mode='MarkdownV2')
            update.message.reply_photo(photo=img)
            context.user_data[State.START_OVER.value] = False
            start.start_callback(update, context)
            return State.END.value