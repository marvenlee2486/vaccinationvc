from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, replymarkup
from telegram.ext import CallbackContext
from telegram.ext.callbackqueryhandler import CallbackQueryHandler
from utils.constants import Authentication, State
from utils.apiService import ApiService
from utils.serializers import AuthenticationSerializer
from utils.errors import catch_error, catch_error_callback_query
from callbacks import start


class Login:

    @staticmethod
    def login_intro_callback(update:Update, context:CallbackContext):
        query = update.callback_query
        keyboard = [
            [
                InlineKeyboardButton(text=Authentication.USERNAME, callback_data=Authentication.USERNAME),
                InlineKeyboardButton(text=Authentication.PASSWORD, callback_data=Authentication.PASSWORD),
            ],
            [
                InlineKeyboardButton(text="Done", callback_data=State.LOGIN_SUBMIT.value),
                InlineKeyboardButton(text="Back", callback_data=State.END.value)
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if "access_token" in context.user_data:
            start.start_callback(update, context)
            return State.END.value
        
        if not context.user_data[State.START_OVER.value]:
            print("SDA")
            query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([]))

            context.user_data["login_data"] = {
                Authentication.USERNAME: None,
                Authentication.PASSWORD: None
            }
            msg = "Lets get some of the information required"
            query.message.reply_text(msg, parse_mode='MarkdownV2', reply_markup=reply_markup)
            print("WA")

        else:
            msg = "Got it\! Please select some feature to update"
            update.message.reply_text(msg, parse_mode='MarkdownV2', reply_markup=reply_markup)
        
        return State.LOGIN_SELECTING_ACTION.value

    @staticmethod
    @catch_error_callback_query
    def login_prompt_info_callback(update:Update, context:CallbackContext):
        query = update.callback_query
        # Empty remove previous inline keyboard
        query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([]))
        feature = query.data
        print(f"feature: {query.data}")
        context.user_data["current_feature"] = feature

        if context.user_data["login_data"].get(feature):
            msg = f"You are updating *{feature}*, type your *{feature}* here"
        else:
            msg = f"Type your *{feature}*"

        query.answer()
        query.message.reply_text(msg, parse_mode='MarkdownV2')

        return State.LOGIN_GET_INFO.value

    @staticmethod
    @catch_error
    def login_get_info_callback(update:Update, context: CallbackContext):

        current_feature = context.user_data.get("current_feature")
        context.user_data["login_data"][current_feature] = update.message.text
        print(f"Updating: {context.user_data.get('login_data')}")

        context.user_data[State.START_OVER.value] = True
        return Login.login_intro_callback(update, context)

    @staticmethod
    @catch_error_callback_query
    def login_submit_info_callback(update: Update, context: CallbackContext):
        query = update.callback_query
        
        login_data = context.user_data["login_data"]
        serializer = AuthenticationSerializer()
        login_data = serializer.dump(login_data)

        username = login_data.get(Authentication.USERNAME)
        password = login_data.get(Authentication.PASSWORD)

        status_code = ApiService.login(username=username, password=password, context=context)

        if status_code == 200:
            msg = "You have login, please enjoy other features\. Going to main page\.\.\.\."
        elif status_code == 400:
            msg = "Incorrect Username or Password\. Going to main page\.\.\.\."
        else:
            msg = "user not found\. Going to main page\.\.\.\."
        query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([]))
        
        del context.user_data["login_data"]
        del context.user_data["current_feature"]

        query.message.reply_text(msg, parse_mode='MarkdownV2')
        
        start.start_callback(update, context)
        context.user_data[State.START_OVER.value] = False
        return State.END.value
        
