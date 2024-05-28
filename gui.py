import csv
import re
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QDateEdit,QLineEdit,QSpacerItem,QSizePolicy
from PySide6.QtWebEngineWidgets import QWebEngineView
from datetime import datetime
from classes import AccidentData

def extract_lat_long(location_str):
    pattern = r'(-?\d+\.\d+),\s*(-?\d+\.\d+)'
    match = re.search(pattern, location_str)
    if match:
        latitude = float(match.group(1))
        longitude = float(match.group(2))
        return latitude, longitude
    else:
        return None, None


location_coordinates = {
    'Bangladesh': (23.6850, 90.3563),
    'Narsingdi': (23.9206, 90.7179),
    'Cumilla': (23.4607, 91.1809),
    'Dhaka': (23.8103, 90.4125),
    'Feni': (23.0238, 91.3976),
    'Kishoreganj': (24.4441, 90.7789),
    'Magura': (23.4892, 89.4168),
    'Taltola': (23.8116, 90.4188),
    'Jigamarir': (25.8123, 89.1234),
    'Gazipur': (24.1051, 90.4072),
    'Karbala': (24.7611, 89.9532),
    'Raipura': (23.9178, 90.7283),
    'Taif': (23.4533, 91.1794),
    'Pathankandi': (24.8768, 91.8555),
    'Mainamati': (23.4667, 91.1833),
    'Roxy': (23.7608, 90.3888),
    'Lalmai': (23.4292, 91.1414),
    'Dagonbhuiyan': (23.0168, 91.4065),
    'Kuliarchar': (24.1183, 90.9519),
    'Habiganj': (24.3814, 91.4160),
    'Khulna': (22.8456, 89.5403),
    'Atharkhada': (23.7250, 90.4250)
}


def extract_single_dates(data):
    month_mapping = {
        "Jan": "January",
        "Feb": "February",
        "March": "March",
        "April": "April",
        "May": "May",
        "June": "June",
        "July": "July",
        "Aug": "August",
        "Sept": "September",
        "Oct": "October",
        "Nov": "November",
        "Dec": "December"
    }
    
    single_dates = []
    for entry in data:
        try:
            date_components = entry.split(' ')
            month = date_components[0]
            day = date_components[1] if len(date_components) > 1 else None
            
            if month[:3].capitalize() in ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]:
                date_string = f"{day}/{month[:3].capitalize()}/2023"
                date_obj = datetime.strptime(date_string, '%d/%b/%Y')
                single_dates.append(date_obj)
            else:
                single_dates.append(None)
        except ValueError:
            single_dates.append(None)

    return single_dates



def read_accident_data_from_csv(file_path):
    accident_data_list = []
    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  
        for row in reader:
            location = row[0].split(";")[0].strip("[]").split(",")[0].strip("'")
            date_str = row[1].split(";")
            date = extract_single_dates(date_str)
            if date is None:
                continue
            
            if "[" in row[2] and "]" in row[2]:
                vehicles_list = row[2].replace("[", "").replace("]", "").replace("'", "").split(",")
                vehicles = ", ".join([vehicle.strip() for vehicle in vehicles_list])
            else:
                print("Unexpected format for vehicles:", row[2])
                vehicles = None
                continue

            casualties_parts = row[3].strip("[]").split(",")
            casualties = [c.strip("'") for c in casualties_parts]
            casualties_age_parts = row[4].strip("[]").split(",")
            casualties_age = [age.strip("'") for age in casualties_age_parts]

        
            if location in location_coordinates:
                latitude, longitude = location_coordinates[location]
            else:
                print("Coordinates not found for location:", location)
                latitude, longitude = None, None
                continue
            
            if latitude is not None and longitude is not None:
                accident = AccidentData(
                    location=(latitude, longitude),
                    date=date,
                    vehicles=vehicles,
                    casualties=None,
                    casualties_age=casualties,
                    injured=None,
                    accident_reason=None,
                    action_sequence=None,
                    link=None,
                    location_name=location
                )
                accident_data_list.append(accident)
            
            for accident in accident_data_list:
                print(accident)

    return accident_data_list


class MapWindow(QMainWindow):
    def __init__(self, accident_data_list):
        super().__init__()
        self.setWindowTitle("Accident Map App")
        self.setGeometry(100, 100, 800, 600)

        self.accident_data_list = accident_data_list
        self.filtered_accidents = accident_data_list.copy()  

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QHBoxLayout(self.central_widget)

        self.filter_tab = QWidget()
        self.filter_layout = QVBoxLayout(self.filter_tab)
        self.filter_tab.setStyleSheet("background-color: #2E5229; padding: 20px;")
        self.filter_layout.setSpacing(0)

        self.start_date_edit = QDateEdit()
        self.start_date_edit.setCalendarPopup(True)
        self.end_date_edit = QDateEdit()
        self.end_date_edit.setCalendarPopup(True)
        self.start_date_edit.setStyleSheet("margin-bottom: 0;")
        

        self.filter_button = QPushButton("Filter")
        self.filter_button.clicked.connect(self.filter_accidents)

        self.clear_filter_button = QPushButton("Clear")
        self.clear_filter_button.clicked.connect(self.clear_filters)

        self.num_vehicles_edit = QLineEdit()
        self.num_casualties_edit = QLineEdit()
        self.num_injured_edit = QLineEdit()
        self.num_vehicles_label = QLabel("Number of Vehicles:")
        self.num_casualties_label = QLabel("Number of Casualties:")
        self.num_injured_label = QLabel("Number of Injured:")
        self.link_label = QLabel("Arcticle Search by Link:")

        self.link_edit = QLineEdit()
        self.extract_accident_button = QPushButton("Extract Accident")
        self.extract_accident_button.clicked.connect(self.extract_accident_from_link)

        layout = QHBoxLayout()

        self.filter_layout.addWidget(self.start_date_edit)
        self.filter_layout.addWidget(self.end_date_edit)
        self.filter_layout.addWidget(self.num_vehicles_label)
        self.filter_layout.addWidget(self.num_vehicles_edit)
        self.filter_layout.addWidget(self.num_casualties_label)
        self.filter_layout.addWidget(self.num_casualties_edit)
        self.filter_layout.addWidget(self.num_injured_label)
        self.filter_layout.addWidget(self.num_injured_edit)
        self.filter_layout.addWidget(self.link_label)
        self.filter_layout.addWidget(self.link_edit)
        self.filter_layout.addWidget(self.extract_accident_button)
        self.filter_layout.addWidget(self.filter_button)
        self.filter_layout.addWidget(self.clear_filter_button)

        self.layout.addWidget(self.filter_tab)

        self.map_widget = QWebEngineView()
        self.layout.addWidget(self.map_widget)

        self.map_widget.setHtml(self.generate_html())
    
    def extract_accident_from_link(self):
        link_text = self.link_edit.text()

        for accident in self.accident_data_list:
            if accident.link == link_text:
                location_match = re.search(r'Location: (.*?);', accident.description)
                if location_match:
                    location = location_match.group(1)
                    print("Location:", location)
                else:
                    print("Location not found in link description")
                break
        else:
            print("Accident not found for link:", link_text)

    def filter_accidents(self):
        start_date = datetime.combine(self.start_date_edit.date().toPython(), datetime.min.time())
        end_date = datetime.combine(self.end_date_edit.date().toPython(), datetime.max.time())
        
        num_vehicles = int(self.num_vehicles_edit.text())
        num_casualties = int(self.num_casualties_edit.text())
        num_injured = int(self.num_injured_edit.text())

        filtered_accidents = [accident for accident in self.accident_data_list 
                              if start_date <= accident.date <= end_date
                              and len(accident.vehicles.split(',')) >= num_vehicles
                              and accident.casualties is not None and accident.casualties >= num_casualties
                              and accident.injured is not None and accident.injured >= num_injured]
        self.filtered_accidents = filtered_accidents
        self.map_widget.setHtml(self.generate_html())

    def clear_filters(self):
        self.filtered_accidents = self.accident_data_list.copy()
        self.start_date_edit.setDate(self.start_date_edit.minimumDate())
        self.end_date_edit.setDate(self.end_date_edit.maximumDate())
        self.map_widget.setHtml(self.generate_html())

    def generate_html(self):
        html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Accident Map</title>
            <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css" />
            <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>
            <style>
                #mapid { 
                    width: 100%;
                    height: 100%;
                    margin: 0;
                    padding: 0;
                }
                body, html {
                    height: 100%;
                    margin: 0;
                    padding: 0;
                }
            </style>
        </head>
        <body>
            <div id="mapid"></div>
            <script>
                var map = L.map('mapid').setView([51.505, -0.09], 13);

                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    maxZoom: 19,
                    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, Imagery &copy; <a href="https://www.mapbox.com/">Mapbox</a>'
                }).addTo(map);
        """

        for accident in self.filtered_accidents:
            html += f"""
                L.marker([{accident.location[0]}, {accident.location[1]}]).addTo(map)
                    .bindPopup('<b>Accident:</b><br>Location: {accident.location_name}<br>Date: {accident.date}<br>Vehicles: {accident.vehicles}<br>Casualties: {accident.casualties}<br>Injured: {accident.injured}<br>Reason: {accident.accident_reason}<br>Action: {accident.action_sequence}<br><a href="{accident.link} ">More info</a>')
                    .openPopup();
            """

        html += """
            </script>
        </body>
        </html>
        """

        return html

    

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # accident_data_list = [
    #     AccidentData(location=(51.5, -0.09), publish_date=datetime.strptime("2024-04-21", "%Y-%m-%d"), update_date="2024-04-21", vehicles=["Car"], casualties=1, casualties_age=None, injured=2, accident_reason="Speeding", action_sequence="Brake failure", link="https://example.com/accident1"),
    #     AccidentData(location=(51.51, -0.1), publish_date=datetime.strptime("2024-04-20", "%Y-%m-%d"), update_date="2024-04-20", vehicles=["Truck", "Car"], casualties=2, casualties_age=None, injured=1, accident_reason="Driver distraction", action_sequence="Sudden lane change", link="https://example.com/accident2"),
    #     AccidentData(location=(51.52, -0.11), publish_date=datetime.strptime("2024-04-19", "%Y-%m-%d"), update_date="2024-04-19", vehicles=["Bike"], casualties=1, casualties_age=None, injured=0, accident_reason="Unsafe lane change", action_sequence="Overtook from wrong side", link="https://example.com/accident3"),
    #     AccidentData(location=(51.53, -0.12), publish_date=datetime.strptime("2024-04-18", "%Y-%m-%d"), update_date="2024-04-18", vehicles=["Bus", "Car"], casualties=3, casualties_age=None, injured=2, accident_reason="Running red light", action_sequence="Failed to stop", link="https://example.com/accident4"),
    #     AccidentData(location=(51.54, -0.13), publish_date=datetime.strptime("2024-04-17", "%Y-%m-%d"), update_date="2024-04-17", vehicles=["Truck"], casualties=1, casualties_age=None, injured=1, accident_reason="Tailgating", action_sequence="Sudden braking", link="https://example.com/accident5"),
    #     AccidentData(location=(51.55, -0.14), publish_date=datetime.strptime("2024-04-16", "%Y-%m-%d"), update_date="2024-04-16", vehicles=["Car", "Car"], casualties=2, casualties_age=None, injured=1, accident_reason="Drowsy driving", action_sequence="Swerved off the road", link="https://example.com/accident6"),
    #     AccidentData(location=(51.56, -0.15), publish_date=datetime.strptime("2024-04-15", "%Y-%m-%d"), update_date="2024-04-15", vehicles=["Car"], casualties=1, casualties_age=None, injured=0, accident_reason="Failure to yield", action_sequence="Crossed without looking", link="https://example.com/accident7"),
    #     AccidentData(location=(51.57, -0.16), publish_date=datetime.strptime("2024-04-14", "%Y-%m-%d"), update_date="2024-04-14", vehicles=["Motorcycle"], casualties=1, casualties_age=None, injured=1, accident_reason="Speeding", action_sequence="Failed to negotiate turn", link="https://example.com/accident8"),
    #     AccidentData(location=(51.58, -0.17), publish_date=datetime.strptime("2024-04-13", "%Y-%m-%d"), update_date="2024-04-13", vehicles=["Car", "Car"], casualties=2, casualties_age=None, injured=1, accident_reason="Texting while driving", action_sequence="Rear-ended", link="https://example.com/accident9"),
    #     AccidentData(location=(51.59, -0.18), publish_date=datetime.strptime("2024-04-12", "%Y-%m-%d"), update_date="2024-04-12", vehicles=["Car"], casualties=1, casualties_age=None, injured=0, accident_reason="Running stop sign", action_sequence="Failed to yield", link="https://example.com/accident10")
    # ]

    accident_data_list = read_accident_data_from_csv("processed_events.csv")
    #accident_data_list = []

    window = MapWindow(accident_data_list)
    window.show()

    sys.exit(app.exec())
