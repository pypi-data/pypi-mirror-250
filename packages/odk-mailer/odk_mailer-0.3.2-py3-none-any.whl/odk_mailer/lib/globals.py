import os

odk_mailer_base = os.path.join(os.getenv("HOME"), ".odk-mailer")
odk_mailer_jobs = os.path.join(odk_mailer_base, "jobs.json")
odk_mailer_job = os.path.join(odk_mailer_base, "job")
path_config = os.path.join(odk_mailer_base, "config.json")