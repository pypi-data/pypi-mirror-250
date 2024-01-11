from odk_mailer.classes.Source import Source
from odk_mailer.classes.Fields import Fields
from odk_mailer.classes.Message import Message
from odk_mailer.classes.Schedule import Schedule

from odk_mailer.lib import globals, utils
import os
import json
from json import JSONEncoder
import hashlib
from types import SimpleNamespace

# return unformatted string instead of raising error
# when key is missing within dictionary
# https://stackoverflow.com/a/17215533/3127170
class SafeDict(dict):
    def __missing__(self, key):
        return '{' + key + '}' 

# custom encoder for JSONEncoder
# https://pynative.com/python-convert-json-data-into-custom-python-object/
class MailjobEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
    
class Mailjob:
    source: Source
    fields: Fields
    message: Message
    schedule: Schedule
    created: int

    hash: str
    json: str

    def __init__(self, hash_or_id = "") -> None:

        if hash_or_id != "":
            self.hash = hash_or_id
            self.hash = self.find()
            self.load()

    def find(self):
        if not self.hash:
            raise Exception("Invalid operation. Hash required")
        
        jobs = self.loadJobsJSON()
        found = next((obj for obj in jobs if obj["hash"].startswith(self.hash)), None)

        if not found:
            utils.abort("Job not found.")        

        return found["hash"]

    def load(self):

        with open(os.path.join(globals.odk_mailer_job, self.hash+'.json'), 'r', encoding='utf-8') as f:
            job = json.load(f, object_hook=lambda d: SimpleNamespace(**d))
        
        # this may be optimized...
        self.source = Source(job.source)
        self.field = Fields(job.fields)
        self.message = Message(job.message)
        self.schedule = Schedule(job.schedule)
        self.recipients = job.recipients

        self.created = job.created


    def create(
        self, 
        source: Source, 
        fields: Fields, 
        message: Message, 
        schedule: Schedule
        ) -> str:

        self.source = source
        self.fields = fields
        self.message = message
        self.schedule = schedule
        self.created = utils.now()

        self.setRecipients()
        self.setJSON()
        self.setHash()

        self.save()
        return self.hash

    def setRecipients(self):
        rows = self.source.get_rows()
        recipients = []
        relevant_fields = self.fields.data + [self.fields.email]
        
        for row in rows:   

            f_row = {k: row[k] for k in relevant_fields }
            recipients.append(f_row)

        self.recipients = recipients

    def save(self):
        # add to job json
        path_to_job = os.path.join(globals.odk_mailer_job, self.hash+'.json')
        with open(path_to_job, 'w', encoding='utf-8') as f:
            f.write(self.json)

        # add to jobs meta
        with open(globals.odk_mailer_jobs, "r+") as f:
            jobs_meta = json.load(f)

            new_job_meta = {
                "hash": self.hash,
                "scheduled": self.schedule.timestamp,
                "recipients": len(self.recipients),
                "state":0
            }
            jobs_meta.append(new_job_meta)
            f.seek(0)
            f.truncate()
            f.write(json.dumps(jobs_meta))
        
        return new_job_meta
    
    def setJSON(self):
        self.json = self.dumpJSON()

    def setHash(self):
        self.hash = hashlib.sha256(self.json.encode()).hexdigest() 

    def dumpJSON(self):
        return json.dumps(vars(self), ensure_ascii=True, indent=4, cls=MailjobEncoder)

    def loadJobsJSON(self):
        with open(globals.odk_mailer_jobs, "r") as f:
            jobs = json.load(f)
        return jobs