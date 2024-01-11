from odk_mailer.classes import Mailjob
from odk_mailer.lib import utils, smtp

from email.message import EmailMessage


class Mailer:
    mailjob: Mailjob
    verbose: bool
    dry: bool

    def __init__(self, dry=False, verbose=False) -> None:
        self.dry = dry
        self.verbose = verbose

    def send(self, mailjob: Mailjob):

        self.mailjob = mailjob

        if self.verbose:
            print("ok")
            print()
            print(f"Run {self.mailjob.hash}")
            print("=====================================================================")
            if self.dry:
                print("Dry Run enabled -no Emails will be sent.")
            else:
                print("Sending emails..")
            print("=====================================================================")


        # Decode base64 if needed
        if self.mailjob.message.source == "stdin":
            text = self.mailjob.message.content
        if self.mailjob.message.source in ["path", "url"]:
            text = utils.base64_decode_str(self.mailjob.message.content)

        if self.dry:
            print()
            print("Message Summary")
            print("-----------------------------------------")
            print(f"sender: {self.mailjob.message.sender}")
            print(f"subject: {self.mailjob.message.subject}")
            print(f"source: {self.mailjob.message.source}")
            print(f"format: {self.mailjob.message.format}")
            print(f"# recipients: {len(self.mailjob.recipients)}")
            print("-----------------------------------------")
            print()

            for idx, recipient in enumerate(self.mailjob.recipients):
                content = utils.safe_format_map(text, recipient)
                print(f"#{idx} ({recipient.email})")
                print()
                print(content)

        else:
            for idx, recipient in enumerate(self.mailjob.recipients):

                content = utils.safe_format_map(text, recipient)

                email = EmailMessage()
                email['From'] = self.mailjob.message.sender
                email['To'] = recipient.email
                email['Subject'] = self.mailjob.message.subject
                email.set_content(content, subtype=self.mailjob.message.format)

                if self.verbose:
                    print()
                    print(f"(#{idx+1}) Attempting to send.. ")

                sent = smtp.send(email, self.verbose, [])

                if sent:
                    # tbd: self.mailjob.setState("success")
                    if self.verbose:
                        print("Success!")

                if not sent:
                    # tbd: self.mailjob.setState("failure")
                    if self.verbose:
                        print("Failure!")