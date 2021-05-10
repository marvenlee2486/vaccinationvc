from telegram.ext import ConversationHandler
from enum import Enum


class State(Enum):

    # State definition for top level conversation
    FEATURE_SELECTION = 1
    # State definitions for 2nd level conversation (features)
    REGISTER = 2
    LOGIN = 3
    ISSUE_VC = 4
    ORG = 121
    ISSUER = 1212132212
    VERIFY = 12252
    # State definition for Register
    REGISTER_SELECTING_ACTION = 5
    REGISTER_GET_INFO = 6
    REGISTER_SUBMIT = 7
    # State definition for Login
    LOGIN_SELECTING_ACTION = 8
    LOGIN_GET_INFO = 9
    LOGIN_SUBMIT = 10
    # State definition for Organization Name
    ORG_SELECTING_ACTION = 11
    ORG_GET_INFO = 12
    # State definition for Issuer Name
    ISSUER_SELECTING_ACTION = 1212
    ISSUER_GET_INFO = 1651
    ISSUER_SUBMIT = 191
    # State definition for Issue Vc
    ISSUERVC_SELECTING_ACTION = 122
    ISSUEVC_GET_INFO = 221
    ISSUEVC_SUBMIT = 4542
    # State definition for Verifying
    VERIFY_GET_INFO =98786576453
    VERIFY_SUBMIT =12312
    # Meta states
    STOPPING = 14
    SHOWING = 15
    START_OVER = 16
    MIDSTATE = 1123121
    # Shortcut to end conversation
    END = ConversationHandler.END


class Authentication:
    USERNAME = "username"
    PASSWORD = "password"
    ORG = "org_name"
    ISSUER = "Issuer_name"
    PATIENT = "patient"
    
class Patient:
    NAME = "name"
    EMAIL = "email"
    