import requests
from telegram.ext import CallbackContext
from utils.config import ENV
import json

class ENDPOINTS:

    SIGNUP = "https://cloud-wallet-api.prod.affinity-project.org/api/v1/users/signup"
    LOGIN = "https://cloud-wallet-api.prod.affinity-project.org/api/v1/users/login"
    BUILD_UNSIGNED_VC = "https://affinity-issuer.prod.affinity-project.org/api/v1/vc/build-unsigned"
    SIGN_CREDENTIAL = "https://cloud-wallet-api.prod.affinity-project.org/api/v1/wallet/sign-credential"
    STORE_CREDENTIAL = "https://cloud-wallet-api.prod.affinity-project.org/api/v1/wallet/credentials"
    VERIFYING_CREDENTIAL = "https://affinity-verifier.prod.affinity-project.org/api/v1/verifier/verify-vcs"

class ApiService:

    @staticmethod
    def signup(username, password, context: CallbackContext):
        '''
            Args: 
            Username: String - Desired username taken from bot interface
            Password: String - Desired password taken from bot interface

            Description: Store did and access token into context object after signing up.

            Returns:
            None
        '''
        header = {
            "Content-Type": "application/json",
            "Api-Key": ENV.API_KEY
        }
        payload = {
            "username": username,
            "password": password
        }
        response = requests.post(ENDPOINTS.SIGNUP, data=json.dumps(payload), headers=header)
        if response.status_code == 200:
            context.user_data["did"] = response.json().get("did")
            context.user_data["access_token"] = response.json().get("accessToken")

        return response.status_code


    @staticmethod
    def login(username, password, context: CallbackContext):
        '''
            Args: 
            username: String - Username from bot interface
            password: String - Password taken from bot interface

            Description: Store did and access token into context object after logging in.

            Returns:
            None
        '''
        header = {
            "Content-Type": "application/json",
            "Api-Key": ENV.API_KEY
        }
        payload = {
            "username": username,
            "password": password
        }
        response = requests.post(ENDPOINTS.LOGIN, data=json.dumps(payload), headers=header)

        if response.status_code == 200:
            context.user_data["did"] = response.json().get("did")
            context.user_data["access_token"] = response.json().get("accessToken")
        
        return response.status_code

    @staticmethod
    def build_unsigned_vc(name, org_name, issuer_name, context: CallbackContext):
        '''
        Args:
        name: String - Name of vaccinated user
        org_name: String - Name of organization that administers the vaccination

        Description: Builds the unsigned VC object

        Returns
        vc: Unsigned VC object
        '''
        header = {
            "Content-Type": "application/json",
            "Api-Key": ENV.API_KEY
        }
        payload = {
            "type": "PhoneCredentialPersonV1",
            "data": {
                "@type": [
                    "Person",
                    "PersonE",
                    "PhonePerson"
                ],
                "telephone": "555 555 5555",
                "name": f'{name} // {issuer_name} // {org_name}'
            },
            "holderDid": context.user_data.get("did")
        }
        response = requests.post(ENDPOINTS.BUILD_UNSIGNED_VC, data=json.dumps(payload), headers=header)
        vc = response.json()
        return vc, response.status_code

    @staticmethod
    def sign_credential(vc, context: CallbackContext):
        '''
        Args:
        vc: String - Unsigned VC object

        Description: Signs the unsigned VC object

        Returns
        vc: Signed VC object
        '''
        header = {
            "Content-Type": "application/json",
            "Api-Key": ENV.API_KEY, 
            "Authorization": context.user_data.get("access_token")
        }
        payload = {
            "unsignedCredential": vc.get("unsignedVC")
        }
        response = requests.post(ENDPOINTS.SIGN_CREDENTIAL, data=json.dumps(payload), headers=header)
        vc = response.json()
        return vc, response.status_code


    @staticmethod
    def store_credential(vc, context: CallbackContext):
        '''
        Args:
        vc: String - Unsigned VC object

        Description: Store signed vc object in the wallet

        Returns
        credential_id: String - Credential id for the signed object now stored in wallet
        '''
        header = {
            "Content-Type": "application/json",
            "Api-Key": ENV.API_KEY, 
            "Authorization": context.user_data.get("access_token")
        }
        payload = {
            "data": [vc.get("signedCredential")]
        }
        
        response = requests.post(ENDPOINTS.STORE_CREDENTIAL, data=json.dumps(payload), headers=header)
        print(response.json())
        credential_id = response.json().get("credentialIds")[0]
        print(credential_id)
        return credential_id, response.status_code

    @staticmethod
    def share_credential(credential_id, context: CallbackContext):
        '''
        Args:
        credential_id: String - Credential id for the signed object now stored in wallet

        Description: Uses share credential endpoint

        Returns
        qr_code: String
        sharing_url: String
        '''
        header = {
            "Content-Type": "application/json",
            "Api-Key": ENV.API_KEY, 
            "Authorization": context.user_data.get("access_token")
        }
        payload = {
            "ttl": "10000000000000"
        }
        response = requests.post(ENDPOINTS.STORE_CREDENTIAL+f"/{credential_id}/share", data=json.dumps(payload), headers=header)
        qr_code = response.json().get("qrCode")
        sharing_url = response.json().get("sharingUrl")
        return qr_code, sharing_url, response.status_code

    @staticmethod
    def verifying_credential(sharing_url, context:CallbackContext):
        header = {
            "Content-Type": "application/json",
            "Api-Key": ENV.API_KEY, 
            "Authorization": context.user_data.get("access_token")
        }
        try:
            response_sharing_url = requests.get(sharing_url, headers=header)
            shared_vc = response_sharing_url.json()

            payload = {
                "verifiableCredentials": shared_vc
            }

            response_verified = requests.post(ENDPOINTS.VERIFYING_CREDENTIAL, data=json.dumps(payload), headers=header)
            if(response_verified.status_code != 200):
                return False
            return response_verified.json()['isValid']
        except:
            return False
