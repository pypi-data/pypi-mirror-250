from odk_mailer.lib import utils, globals
from types import SimpleNamespace
import json
import os

class Config():
    odk_host: str
    smtp_host: str
    smtp_port: str
    smtp_user: str
    smtp_pass: str
    
    def __init__(self):
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

            self.odk_host =  config.odk_host

            self.smtp_host = config.smtp_host
            self.smtp_port = config.smtp_port

            # optional config parameters
            if hasattr(config, "smtp_user"):
                self.smtp_user = config.smtp_user
            else:
                self.smtp_user = None
            if hasattr(config, "smtp_pass"):
                self.smtp_pass = config.smtp_pass
            else:
                self.smtp_pass = None