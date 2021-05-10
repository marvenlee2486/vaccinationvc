from telegram.ext import ConversationHandler
from enum import Enum


class State(Enum):

    # State definition for top level conversation
    FEATURE_SELECTION = 1
    # State definitions for 2nd level conversation (features)
    REGISTER = 2
    LOGIN = 3
    ISSUE_VC = 4
    ORG = 5
    ISSUER = 6
    VERIFY = 7
    # State definition for Register
    REGISTER_SELECTING_ACTION = 8
    REGISTER_GET_INFO = 9
    REGISTER_SUBMIT = 10
    # State definition for Login
    LOGIN_SELECTING_ACTION = 11
    LOGIN_GET_INFO = 12
    LOGIN_SUBMIT = 13
    # State definition for Organization Name
    ORG_SELECTING_ACTION = 14
    ORG_GET_INFO = 15
    # State definition for Issuer Name
    ISSUER_SELECTING_ACTION = 16
    ISSUER_GET_INFO = 17
    ISSUER_SUBMIT = 18
    # State definition for Issue Vc
    ISSUERVC_SELECTING_ACTION = 19
    ISSUEVC_GET_INFO = 20
    ISSUEVC_SUBMIT = 21
    # State definition for Verifying
    VERIFY_GET_INFO =22
    VERIFY_SUBMIT =23
    # Meta states
    STOPPING = 24
    SHOWING = 25
    START_OVER = 26
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
    