from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, replymarkup
from telegram.ext import CallbackContext
from telegram.ext.callbackqueryhandler import CallbackQueryHandler
from utils.constants import Authentication, State
from utils.apiService import ApiService
from utils.serializers import AuthenticationSerializer
from utils.errors import catch_error, catch_error_callback_query
from callbacks import start


class Register:

    @staticmethod
    def register_intro_callback(update:Update, context:CallbackContext):
        query = update.callback_query
        keyboard = [
            [
                InlineKeyboardButton(text=Authentication.USERNAME, callback_data=Authentication.USERNAME),
                InlineKeyboardButton(text=Authentication.PASSWORD, callback_data=Authentication.PASSWORD),
            ],
            [
                InlineKeyboardButton(text="Done", callback_data=State.REGISTER_SUBMIT.value),
                InlineKeyboardButton(text="Back", callback_data=State.END.value)
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        print(context.user_data[State.START_OVER.value])
        if "access_token" in context.user_data:
            start.start_callback(update, context)
            return State.END.value
        print(context.user_data[State.START_OVER.value])
        print(context.user_data[State.START_OVER.value])
        print(context.user_data[State.START_OVER.value])
        print(context.user_data[State.START_OVER.value])
        if not context.user_data[State.START_OVER.value]:
            print("HIDAHSFIAHFKLAFIJK")
            query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([]))

            context.user_data["registration_data"] = {
                Authentication.USERNAME: None,
                Authentication.PASSWORD: None
            }
            msg = "Lets get some of the information required"
            query.message.reply_text(msg, parse_mode='MarkdownV2', reply_markup=reply_markup)

        else:
            msg = "Got it\! Please select some feature to update"
            update.message.reply_text(msg, parse_mode='MarkdownV2', reply_markup=reply_markup)
        
        return State.REGISTER_SELECTING_ACTION.value

    @staticmethod
    @catch_error_callback_query
    def register_prompt_info_callback(update:Update, context:CallbackContext):
        query = update.callback_query
        # Empty remove previous inline keyboard
        query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([]))
        feature = query.data
        print(f"feature: {query.data}")
        context.user_data["current_feature"] = feature

        if context.user_data["registration_data"].get(feature):
            msg = f"You are updating *{feature}*, type your *{feature}* here"
        else:
            msg = f"Type your *{feature}*"

        query.answer()
        query.message.reply_text(msg, parse_mode='MarkdownV2')

        return State.REGISTER_GET_INFO.value

    @staticmethod
    @catch_error
    def register_get_info_callback(update:Update, context: CallbackContext):

        current_feature = context.user_data.get("current_feature")
        context.user_data["registration_data"][current_feature] = update.message.text
        print(f"Updating: {context.user_data.get('registration_data')}")

        context.user_data[State.START_OVER.value] = True
        return Register.register_intro_callback(update, context)

    @staticmethod
    @catch_error_callback_query
    def register_submit_info_callback(update: Update, context: CallbackContext):
        query = update.callback_query
        
        registration_data = context.user_data["registration_data"]
        serializer = AuthenticationSerializer()
        registration_data = serializer.dump(registration_data)

        username = registration_data.get(Authentication.USERNAME)
        password = registration_data.get(Authentication.PASSWORD)

        status_code = ApiService.signup(username=username, password=password, context=context)
        print(status_code)
        if status_code == 200:
            msg = "Registered, please login to enjoy other features\. Returning to main menu\.\.\.\."
        elif status_code == 409:
            msg = "The Username is registered, please try to another username\. Returning to main menu\.\.\.\."
        else:
            msg = "Bad request\. Returning to main menu\.\.\.\." 
        query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([]))
        del context.user_data["registration_data"]
        del context.user_data["current_feature"]

        query.message.reply_text(msg, parse_mode='MarkdownV2')
        
        start.start_callback(update, context)
        context.user_data[State.START_OVER.value] = False
        return State.END.value
        