from callbacks.verify import Verify
from callbacks.details import Org
from callbacks.details import Issuer
from callbacks.issuevc import IssueVc
from callbacks.login import Login
import logging
from telegram.ext import Updater, Filters
from telegram.ext.conversationhandler import ConversationHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.callbackqueryhandler import CallbackQueryHandler
from utils.constants import Authentication, State, Patient
from utils.config import ENV

from callbacks import start, stop, back_main_menu
from callbacks.register import Register

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

def main():
    updater = Updater(token=ENV.BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    
    #TODO: Convo Handler for register
    register_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(Register.register_intro_callback, pattern=f"^{str(State.REGISTER.value)}$")],
        states={
            State.REGISTER_SELECTING_ACTION.value: [
                CallbackQueryHandler(
                    Register.register_prompt_info_callback, 
                    pattern=f"^{Authentication.USERNAME}|{Authentication.PASSWORD}$"
                )
            ],
            State.REGISTER_GET_INFO.value: [
                MessageHandler(
                    Filters.text & ~Filters.command,
                    Register.register_get_info_callback
                )
            ]
        },
        fallbacks=[
            CommandHandler("stop", stop.stop_callback),
            CallbackQueryHandler(
                back_main_menu.back_main_menu_callback,
                pattern=f"^{str(State.END.value)}$"
            ),
            CallbackQueryHandler(
                Register.register_submit_info_callback,
                pattern=f"^{State.REGISTER_SUBMIT.value}$"
            )
        ]
    )
    #TODO: Convo Handler for login 
    login_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(Login.login_intro_callback, pattern=f"^{str(State.LOGIN.value)}$") ],
        states={
            State.LOGIN_SELECTING_ACTION.value: [
                CallbackQueryHandler(
                    Login.login_prompt_info_callback, 
                    pattern= f"^{Authentication.USERNAME}|{Authentication.PASSWORD}$"
                )
            ],
            State.LOGIN_GET_INFO.value: [
                MessageHandler(
                    Filters.text & ~Filters.command,
                    Login.login_get_info_callback
                )
            ]

        },
        fallbacks=[
            CommandHandler("stop", stop.stop_callback),
            CallbackQueryHandler(
                back_main_menu.back_main_menu_callback,
                pattern=f"^{str(State.END.value)}$"
            ),
            CallbackQueryHandler(

                Login.login_submit_info_callback,
                pattern=f"^{State.LOGIN_SUBMIT.value}$"
            )
        ]
    )
    org_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(Org.Org_prompt_info_callback, pattern=f"^{str(State.ORG.value)}$") ],
        states={
            State.ORG_GET_INFO.value: [
                MessageHandler(
                    Filters.text & ~Filters.command,
                    Org.Org_get_info_callback
                )
            ]

        },
        fallbacks=[
            CommandHandler("stop", stop.stop_callback),
            CallbackQueryHandler(
                back_main_menu.back_main_menu_callback,
                pattern=f"^{str(State.END.value)}$"
            )
        ]
    )
    issuer_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(Issuer.Issuer_prompt_info_callback, pattern=f"^{str(State.ISSUER.value)}$") ],
        states={
            State.ISSUER_GET_INFO.value: [
                MessageHandler(
                    Filters.text & ~Filters.command,
                    Issuer.Issuer_get_info_callback
                )
            ]

        },
        fallbacks=[
            CommandHandler("stop", stop.stop_callback),
            CallbackQueryHandler(
                back_main_menu.back_main_menu_callback,
                pattern=f"^{str(State.END.value)}$"
            )
        ]
    )
    #TODO: Convo Handler for issuing
    issue_vc_conv = ConversationHandler(    
        entry_points=[CallbackQueryHandler(IssueVc.issue_intro_callback, pattern=f"^{str(State.ISSUE_VC.value)}$") ],
        states={
            State.ISSUER_SELECTING_ACTION.value: [
                CallbackQueryHandler(
                    IssueVc.issue_prompt_info_callback,
                    pattern= f"^{Patient.NAME}|{Patient.EMAIL}$"
                )
            ],
            State.ISSUEVC_GET_INFO.value: [
                MessageHandler(
                    Filters.text & ~Filters.command,
                    IssueVc.issue_get_info_callback
                )
            ],
        },
        fallbacks=[
            CommandHandler("stop", stop.stop_callback),
            CallbackQueryHandler(
                back_main_menu.back_main_menu_callback,
                pattern=f"^{str(State.END.value)}$"
            ),
            CallbackQueryHandler(
                IssueVc.issue_submit_info_callback,
                pattern=f"^{State.ISSUEVC_SUBMIT.value}$"
            )
        ]
    )
    verify_conv = ConversationHandler(
        entry_points = [CallbackQueryHandler(Verify.verify_prompt_info_callback, pattern = f"^{str(State.VERIFY.value)}$") ],
        states={
            State.VERIFY_GET_INFO.value: [
                MessageHandler(
                    Filters.text & ~Filters.command,
                    Verify.verify_get_info_callback
                )
            ],
        },
        fallbacks=[
            CommandHandler("stop", stop.stop_callback),
            CallbackQueryHandler(
                back_main_menu.back_main_menu_callback,
                pattern=f"^{str(State.END.value)}$"
            ),
            CallbackQueryHandler(
                Verify.verify_submit_info_callback,
                pattern=f"^{State.VERIFY_SUBMIT.value}$"
            )
        ]
    )

    # main convo handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start.start_callback)],
        states={
            # State.SHOWING.value: [CallbackQueryHandler(start.start_callback, pattern=f"^{str(State.END.value)}$")],
            State.FEATURE_SELECTION.value: [
                ### UNCOMMENT IF DONE ###
                register_conv,
                login_conv,
                org_conv,
                issuer_conv,
                issue_vc_conv,
                verify_conv,
            ],
        },
        fallbacks=[CommandHandler("stop", stop.stop_callback)]
    )
    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()