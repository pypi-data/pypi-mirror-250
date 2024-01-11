import csv
class Source:
    type: str
    location: str
    project: int    
    hostname: str
    username: str
    password: str

    def __init__(self, data: []):

        self.type = data["type"]

        if self.type == "path":
            self.location = data["location"]
        
        if self.type == "url":
            self.location = data["location"]

        if self.type == "api":
            self.location = data["location"]
            self.project = data["api_proj"]
            self.hostname = data["api_host"]
            self.username = data["api_user"]
            self.password = data["api_pass"]

    def get_headers(self):            
        if self.type == 'path':        
            with open(self.location, newline='') as f:
                reader = csv.DictReader(f, skipinitialspace=True)
                headers = reader.fieldnames
            return headers
        
        

    def get_rows(self):
        if self.type == 'path':        
            with open(self.location, newline='') as f:
                reader = csv.DictReader(f, skipinitialspace=True)
                #headers = reader.fieldnames
                rows = []
                for row in reader:
                    rows.append(row)

            return rows
        
        raise Exception("Source type is not yet implemented" )
       