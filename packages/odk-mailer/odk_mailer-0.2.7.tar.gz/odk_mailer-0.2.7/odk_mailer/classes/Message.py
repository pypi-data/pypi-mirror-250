class Message:
    sender: str
    subject: str
    source: str
    content: str
    format: str

    def __init__(self, data: []) -> None:

        self.sender = data["sender"]
        self.subject = data["subject"]
        self.source = data["source"]
        self.format = data["type"]
        
        if self.source == "stdin":
            self.content = data["content"]

        if self.source == "path":
            # tbd: read from file and store as base64
            self.content = data["content"]

        if self.source == "url":
            #tbd: read from url and store as base64
            self.content = data["content"]
                    