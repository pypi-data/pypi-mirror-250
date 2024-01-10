from odk_mailer.classes import Source, Fields, Message, Schedule
from odk_mailer.lib import globals
import sys
import os
import json
import hashlib

class Mailjob:
    source: Source
    fields: Fields
    message: Message
    schedule: Schedule

    hash: str
    json: str

    def __init__(hash_or_id = "") -> None:
        pass

    def createFrom(self, source: Source, fields: Fields, message: Message, schedule: Schedule) -> str:

        self.source = source
        self.fields = fields
        self.message = message
        self.schedule = schedule

        self.setRecipients()
        self.setJSON()
        self.setHash()

        return self.hash


    def setRecipients(self):
        rows = self.source.get_rows()
        recipients = []
        relevant_fields = self.fields.data + [self.fields.email]
        
        # print(relevant_fields)
        # print(rows[0])
        # sys.exit()
        for row in rows:   

            f_row = {k: row[k] for k in relevant_fields }
            recipients.append(f_row)

        self.recipients = recipients

    def save(self):

        sys.exist()
        # save files
        path_to_job = os.path.join(globals.odk_mailer_job, self.hash+'.json')
        with open(path_to_job, 'w', encoding='utf-8') as f:
            f.write(self.json)

        with open(globals.odk_mailer_jobs, "r+") as f:
            jobs = json.load(f)
            save_job = {
                "hash": self.hash,
                "scheduled": self.schedule,
                "recipients": len(self.recipients),
                "state":0
            }
            jobs.append(save_job)
            f.seek(0)
            f.truncate()
            f.write(json.dumps(jobs))

    def setJSON(self):

        self.json = json.dumps(vars(self), ensure_ascii=True, indent=4)

    def setHash(self):
        self.hash = hashlib.sha256(self.json.encode()).hexdigest()


    