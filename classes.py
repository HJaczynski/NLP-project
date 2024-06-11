class AccidentData:
    def __init__(self, location, date, vehicles, casualties, casualties_age, injured, accident_reason, action_sequence, link,location_name = "NA", exact_location_name="NA"):
        self.location = location
        self.date = date
        self.vehicles = vehicles
        self.casualties = casualties
        self.casualties_age = casualties_age
        self.injured = injured
        self.accident_reason = accident_reason
        self.action_sequence = action_sequence
        self.link = link
        self.exact_location_name = exact_location_name
    
    def __str__(self):
        return f"Accident Data: Location={self.location}, Date={self.date}, Vehicles={self.vehicles}, Casualties={self.casualties}, Casualties Age={self.casualties_age},  Injured={self.injured}, Reason={self.accident_reason}, Action={self.action_sequence}, Link={self.link}"



class MetaData:
    def __init__(self, publication_date, update_date, meta_location, title, html_text, raw_text, link):
        self.publication_date = publication_date
        self.update_date = update_date
        self.meta_location = meta_location
        self.title = title
        self.HTML_text = html_text
        self.raw_text = raw_text
        self.link = link
        
    def __str__(self):
        return f"Title: {self.title} \nPublication Date: {self.publication_date} \nUpdate Date: {self.update_date} \nLocation: {self.meta_location} \nLink: {self.link}\n"
