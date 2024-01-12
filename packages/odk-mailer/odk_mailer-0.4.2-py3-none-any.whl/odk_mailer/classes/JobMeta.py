class JobMeta:
    hash: str
    created: int
    scheduled: int
    recipients: int
    state: int

    def __init__(self, mailjob) -> None:
        
        self.hash = mailjob.hash
        self.created = mailjob.created
        self.scheduled = mailjob.schedule.timestamp
        self.recipients = len(mailjob.recipients)
        self.state = 0