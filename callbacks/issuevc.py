from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, replymarkup
from telegram.ext import CallbackContext
from utils.constants import Authentication, State, Patient
from utils.apiService import ApiService
from utils.errors import catch_error, catch_error_callback_query
from utils.emailService import email_service
from callbacks import start


class IssueVc:

    @staticmethod
    def issue_intro_callback(update:Update, context:CallbackContext):
        query = update.callback_query
        # Empty remove previous inline keyboard
        
        print("feature: org_name")
        if( not context.user_data.get("org_name")):
            context.user_data[State.START_OVER.value] = True
            msg = "No organization name found, please update your organization name\."
            query.message.reply_text(msg, parse_mode='MarkdownV2')
            start.start_callback(update, context)
            return State.END.value
            
        
        print("feature: Issuer_name")
        if (not context.user_data.get("Issuer_name")):
            context.user_data[State.START_OVER.value] = True
            msg = "No issuer name found, please update your organization name\."
            query.message.reply_text(msg, parse_mode='MarkdownV2')
            start.start_callback(update, context)
            return State.END.value

        msg = "Update the following details as shown below"
        keyboard = [
            [
                InlineKeyboardButton("Name of patient", callback_data=Patient.NAME),
                InlineKeyboardButton("Email of patient", callback_data=Patient.EMAIL)
            ],
            [
                InlineKeyboardButton(text="Done", callback_data=State.ISSUEVC_SUBMIT.value),
                InlineKeyboardButton(text="Back", callback_data=State.END.value)
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        if not context.user_data[State.START_OVER.value]:
            query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([]))
            context.user_data["patient_data"] = {
                Patient.NAME: None,
                Patient.EMAIL: None
            }
            msg = "Lets get some of the information required"
            query.message.reply_text(msg, parse_mode='MarkdownV2', reply_markup=reply_markup)

        else:

            msg = "Got it\! Please select some feature to update"
            update.message.reply_text(msg, parse_mode='MarkdownV2', reply_markup=reply_markup)

        return State.ISSUER_SELECTING_ACTION.value

    @staticmethod
    @catch_error_callback_query
    def issue_prompt_info_callback(update:Update, context:CallbackContext):
        query = update.callback_query
        # Empty remove previous inline keyboard
        query.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup([]))
        feature = query.data
        print(f"feature: {query.data}")
        context.user_data["current_feature"] = feature

        if context.user_data["patient_data"].get(feature):
            msg = f"You are updating *{feature}*, type your *{feature}* here"
        else:
            msg = f"Type your *{feature}*"

        query.answer()
        query.message.reply_text(msg, parse_mode='MarkdownV2')

        return State.ISSUEVC_GET_INFO.value

    @staticmethod
    def issue_get_info_callback(update:Update, context: CallbackContext):
        
        current_feature = context.user_data.get("current_feature")
        context.user_data["patient_data"][current_feature] = update.message.text
        print(f"Updating: {context.user_data.get('patient_data')}")

        context.user_data[State.START_OVER.value] = True
        return IssueVc.issue_intro_callback(update, context)

    

    @staticmethod
    @catch_error_callback_query
    def issue_submit_info_callback(update: Update, context: CallbackContext):
        
        org = context.user_data.get(Authentication.ORG)
        issuer = context.user_data.get(Authentication.ISSUER)
        patient_data = context.user_data.get("patient_data")

        patient_name = patient_data.get(Patient.NAME)
        patient_email = patient_data.get(Patient.EMAIL)
        if not patient_name or not patient_email:
            context.user_data[State.START_OVER.value] = False
            msg = "You have not enter patient name or patient email, please enter them \."
            update.callback_query.message.reply_text(msg, parse_mode='MarkdownV2')
            return IssueVc.issue_intro_callback(update, context)


        vc, status_code = ApiService.build_unsigned_vc(name=patient_name, issuer_name=issuer, org_name=org, context=context)

        if status_code != 200:
            print(f"Something went wrong with building unsigned VC, status code: {status_code}")
            pass

        vc, status_code = ApiService.sign_credential(vc=vc, context=context)

        if status_code != 200:
            print(f"Something went wrong with signing VC, status code: {status_code}")
            pass

        credential_id, status_code = ApiService.store_credential(vc=vc, context=context)

        if('credential' not in context.user_data.keys()):
            context.user_data['credential']= {}
        context.user_data['credential'][patient_name] = credential_id

        print("Store" , status_code)
        if status_code != 200:
            print(f"Something went wrong with storing VC, status code: {status_code}")
            pass

        qr_code, sharing_url, status_code = ApiService.share_credential(credential_id, context)

        if status_code == 200:
            email_service(sharing_url, qr_code, patient_email)
            msg = "Registered VC and VC is signed and stored\. Returning to main menu\.\.\.\."
            del context.user_data["patient_data"]
            del context.user_data["current_feature"]

            update.callback_query.message.reply_text(msg, parse_mode='MarkdownV2')
            context.user_data[State.START_OVER.value] = True
            start.start_callback(update, context)
            return State.END.value