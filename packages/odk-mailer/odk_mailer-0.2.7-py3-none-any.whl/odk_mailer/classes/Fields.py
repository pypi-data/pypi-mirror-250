class Fields:
    email: str
    data: []

    def __init__(self, data: []):
            
        self.email = data["email"]
        if "data" in data:
            self.data = data["data"]
        else:
            self.data = []