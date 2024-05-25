class AccidentData:
    def __init__(self, location, date, vehicles, casualties, casualties_age, injured, accident_reason, action_sequence, link):
        self.location = location
        self.date = date
        self.vehicles = vehicles
        self.casualties = casualties
        self.casualties_age = casualties_age
        self.injured = injured
        self.accident_reason = accident_reason
        self.action_sequence = action_sequence
        self.link = link


class MetaData:
    def __init__(self, publication_date, update_date, meta_location, title, html_text, raw_text, link):
        self.publication_date = publication_date #done
        self.update_date = update_date #done
        self.meta_location = meta_location #done
        self.title = title #done
        self.HTML_text = html_text #done
        self.raw_text = raw_text #done
        self.link = link #done

    def __str__(self):
        return f"Title: {self.title} \nPublication Date: {self.publication_date} \nUpdate Date: {self.update_date} \nLocation: {self.meta_location} \nLink: {self.link}\n"
