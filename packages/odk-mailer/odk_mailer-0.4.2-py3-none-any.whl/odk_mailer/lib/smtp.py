from odk_mailer.classes.Config import Config
import smtplib

def send(email, verbose=False, config=[]):
    
    if not config:

        odk_mailer_config = Config()
        if not odk_mailer_config:
            raise Exception("Fatal Error: No Configuration File found.")

        smtp_host = odk_mailer_config.smtp_host
        smtp_port = odk_mailer_config.smtp_port
        smtp_user = odk_mailer_config.smtp_user
        smtp_pass = odk_mailer_config.smtp_pass
    else: 
        smtp_host, smtp_port, smtp_user, smtp_pass = config

    try:            
        smtp = smtplib.SMTP(timeout=5)
        if verbose:
        # enable debugging by CLI flag --debug
            smtp.set_debuglevel(2)

        smtp.connect(smtp_host, smtp_port)

        if smtp_user and smtp_pass:
        # if username and password are supplied, smtp.login()            
            smtp.login(smtp_user, smtp_pass)
        
        smtp.send_message(email)
        smtp.quit()

        if verbose:
            print()
            print("Successfully sent email to " + email["To"])
            print()
        # write into /log/timestamp_<hash>.log
        # tbd: log.write("Successfully sent email to " + email["To"])
        return True
    except Exception as error:

        if verbose:
            # write into /log/timestamp_<hash>.log
            # raise exception to interrupt loop
            print(error)
            print("Failed sending mail to: " + email['To'])
            print()
        
        return False