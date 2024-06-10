class AccidentData:
<<<<<<< Updated upstream
    def __init__(self, location, publish_date, update_date, vehicles, casualties, casualties_age, injured, accident_reason, action_sequence, link):
=======
    def __init__(self, location, date, vehicles, casualties, casualties_age, injured, accident_reason, action_sequence, link,exact_location_name):
>>>>>>> Stashed changes
        self.location = location
        self.publish_date = publish_date
        self.update_date = update_date
        self.vehicles = vehicles
        self.num_vehicles = len(self.vehicles)
        self.casualties = casualties
        self.casualties_age = casualties_age
        self.injured = injured
        self.accident_reason = accident_reason
        self.action_sequence = action_sequence
        self.link = link
<<<<<<< Updated upstream
=======
        self.exact_location_name = exact_location_name
        
    
    def __str__(self):
        return f"Accident Data: Location={self.location}, Date={self.date}, Vehicles={self.vehicles}, Casualties={self.casualties}, Injured={self.injured}, Reason={self.accident_reason}, Action={self.action_sequence}, Link={self.link}"

>>>>>>> Stashed changes


class MetaData:
    def __init__(self, publication_date, update_date, meta_location, title, html_text, raw_text, link):
        self.publication_date = publication_date #done
        self.update_date = update_date #done
        self.meta_location = meta_location #done
        self.title = title #done
        self.HTML_text = html_text #done
        self.raw_text = raw_text #done
        self.link = link #done

    # def __str__(self):
    #     return f"Title: {self.title} \nPublication Date: {self.publication_date} \nUpdate Date: {self.update_date} \nLocation: {self.meta_location} \nLink: {self.link}\n"

    def __str__(self):
<<<<<<< Updated upstream
        return f"Title: {self.title} \nPublication Date: {self.publication_date} \nUpdate Date: {self.update_date} \nLocation: {self.meta_location} \nLink: {self.link}\n"
=======
        return f"raw_text: {self.raw_text} "
>>>>>>> Stashed changes
