from odk_mailer.lib import utils, globals
from types import SimpleNamespace
import json
import os
import sys

class Config():
    odk_host: str
    smtp_host: str
    smtp_port: str
    smtp_user: str
    smtp_pass: str
    
    def __init__(self, smtpRequired:bool=False, odkRequired:bool=False):

        # #load_dotenv()

        # ODK_HOST = os.getenv('ODK_HOST')
        # print(ODK_HOST)
        # SMTP_HOST = os.getenv('SMTP_HOST')
        # print(SMTP_HOST)
        # SMPT_PORT = os.getenv('SMTP_PORT')
        # SMPT_USER = os.getenv('SMPT_USER')
        # SMPT_PASS = os.getenv('SMPT_PASS')

        # if smtpRequired:
        #     if not SMTP_HOST or not SMPT_PORT:
        #         utils.abort("Config Error: SMTP_HOST and SMPT_PORT are required configuration for sending emails.")

        # if odkRequired and not ODK_HOST:
        #     utils.abort("Config Error: ODK_Host is required configuration for accessing ODK API.")

        # self.smtp_host = SMTP_HOST
        # self.smtp_port = SMPT_PORT
        # self.smtp_user = SMPT_USER
        # self.smtp_pass = SMPT_PASS

        # self.odk_host = ODK_HOST        
    
        if os.path.exists(globals.path_config):
            with open(globals.path_config, "r") as f:
                config = json.load(f, object_hook=lambda d: SimpleNamespace(**d))
            
            if not config:
                utils.abort("Config Error: Check .odk-mailer/config.json ")

            #required_keys = ["odk_host", "smtp_host", "smtp_port"]
            required_keys = ["smtp_host", "smtp_port"]

            for required_key in required_keys:
                if not required_key in vars(config):                
                    utils.abort(f"Invalid config: Key '{required_key}' is required.")

            self.smtp_host = config.smtp_host
            self.smtp_port = config.smtp_port

            if hasattr(config, "smtp_host"):
                self.odk_host =  config.odk_host

            # optional config parameters
            if hasattr(config, "smtp_user"):
                self.smtp_user = config.smtp_user
            else:
                self.smtp_user = None
            if hasattr(config, "smtp_pass"):
                self.smtp_pass = config.smtp_pass
            else:
                self.smtp_pass = None