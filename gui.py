import csv
import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QDateEdit,QLineEdit,QSizePolicy
from PySide6.QtWebEngineWidgets import QWebEngineView
from datetime import datetime
from classes import AccidentData


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
    'Atharkhada': (23.7250, 90.4250),
    'Mirpur': (23.8103, 90.3660),
    "Chattogram": (22.3569, 91.7832),
    "Munshiganj": (23.5422, 90.5305),
    "Rangamati": (22.6276, 92.2236),
    "Chandraghona": (22.4895, 92.1018),
    "Chowgachha": (23.4659, 89.0242),
    "Sumona": (23.7806, 90.2792),
    "Sherpur": (25.0187, 90.0153),
    "Nilphamari": (25.9310, 88.8560),
    "Chonka": (25.8504, 88.8743),
    "Senbagh Upazila": (22.9441, 91.2924),
    "Sharsha": (23.0159, 88.8713),
    "Durgapur": (24.9701, 88.7558),
    "Ullapara": (24.3379, 89.5811),
    "Sardia": (23.7745, 90.4151),
    "Boalmari": (23.3158, 89.6342),
    "Faridpur": (23.6076, 89.8342),
    "Rubel": (23.7806, 90.2792),
    "Belkuchi": (24.2616, 89.6943),
    "Shahjahanpur": (24.7791, 89.3121),
    "Daudkandi": (23.5337, 90.7192),
    "Kushiara": (24.0907, 90.3971),
    "Bikrampur": (23.5433, 90.5327),
    "Sirajganj": (24.4534, 89.7083),
    "Chapainawabganj": (24.5964, 88.2775),
    "Bhola": (22.6859, 90.6482),
    "Karimpur": (23.7748, 90.4010),
    "Sonargaon": (23.6453, 90.5994),
    "Sadar Upazila": (24.0850, 90.8765),
    "Rahela": (23.7806, 90.2792),
    "Tetulia": (26.6654, 88.4174),
    "Nirwarispur": (24.1187, 90.7645),
    "Begumganj Upazila": (22.9916, 91.0874),
    "Armanitola": (23.7111, 90.4038),
    "Minhaj": (23.7806, 90.2792),
    "Gopalganj": (23.0052, 89.8266),
    "Barguna": (22.1514, 90.1263),
    "Barera": (23.7806, 90.2792),
    "Palpara": (23.7806, 90.2792),
    "Wasi": (23.7806, 90.2792),
    "Salna": (24.1286, 90.4192),
    "Chandpur": (23.2330, 90.6638),
    "Rajshahi": (24.3745, 88.6042),
    "Manikganj": (23.8644, 90.0047),
    "Jagir": (23.7806, 90.2792),
    "Boliarpur": (23.8492, 90.0132),
    "Dinajpur": (25.6279, 88.6331),
    "Darikandi": (23.7806, 90.2792),
    "Chiura": (23.7806, 90.2792),
    "Senbagh upazila": (22.9441, 91.2924),
    "Sharsha": (23.0159, 88.8713),
    "Chapainawabganj": (24.5964, 88.2775),
    "Bhola": (22.6859, 90.6482),
    "Karimpur": (23.7748, 90.4010),
    "Sonargaon": (23.6453, 90.5994),
    "Sadar Upazila": (24.0850, 90.8765),
    "Rahela": (23.7806, 90.2792),
    "Tetulia": (26.6654, 88.4174),
    "Nirwarispur": (24.1187, 90.7645),
    "Begumganj Upazila": (22.9916, 91.0874),
    "Armanitola": (23.7111, 90.4038),
    "Minhaj": (23.7806, 90.2792),
    "Gopalganj": (23.0052, 89.8266),
    "Barguna": (22.1514, 90.1263),
    "Barera": (23.7806, 90.2792),
    "Palpara": (23.7806, 90.2792),
    "Wasi": (23.7806, 90.2792),
    "Salna": (24.1286, 90.4192),
    "Chandpur": (23.2330, 90.6638),
    "Rajshahi": (24.3745, 88.6042),
    "Manikganj": (23.8644, 90.0047),
    "Jagir": (23.7806, 90.2792),
    "Boliarpur": (23.8492, 90.0132),
    "Dinajpur": (25.6279, 88.6331),
    "Darikandi": (23.7806, 90.2792),
    'Karnaphuli': (22.3159, 91.8364),
    'Naogaon': (24.7936, 88.9561),
    'Saidabad': (23.6667, 90.4167),
    'Patnitola': (24.6317, 88.0756),
    'Jhenaidah': (23.5448, 89.1531),
    'Juktitala': (23.8846, 90.7158),
    'Karnopur': (24.7500, 88.8500),
    'Nahid': (24.3217, 90.5691),
    'Utkura': (23.9567, 90.6056),
    'Sitakunda': (22.5570, 91.7848),
    'Tarapur': (24.5908, 88.0886),
    'Sheora': (24.3439, 89.9282),
    "Thakurgaon": (26.0388, 88.4617),
    "Pranta Hossain": (24.9050, 89.0506),
    "Chuadanga": (23.6414, 88.8566),
    "Kajikanda": (23.9011, 89.1923),
    "Chatmohor": (24.8416, 88.9664),
    "Bathuli": (24.7632, 89.3753),
    "Sonatunia": (24.2203, 88.9118),
    "Pirganj upazila": (25.8610, 88.4277),
    "Shariatpur": (23.2423, 90.4283),
    "Nimanur": (24.6114, 89.9427),
    "Shahbagh": (23.7395, 90.3854),
    "Sadar upazila": (24.0850, 90.8765),
    "Chandrapara": (24.5667, 88.4167),
    "Manisha": (24.3586, 88.7875),
    "Rampal": (22.6020, 89.7663),
    "Namo Mingachha": (23.5000, 90.0500),
    "South Bashabo": (23.7140, 90.4455),
    "Netrakona": (24.8707, 90.7275),
    "Boilgram": (24.7488, 88.8268),
    'Karwanbazar': (23.7513, 90.4060),
    'Pabna': (24.0083, 89.2431),  
    'Hatia': (22.3039, 91.1033),  
    'Mahbub': (24.9079, 88.2610),  
    'West Rabishur': (23.8354, 90.1647),  
    'Hatijheel': (23.7402, 90.4094), 
    'Dauladia': (23.3731, 89.8073), 
    'Saidpur': (25.7789, 88.8915), 
    'Alalpur': (24.0583, 89.8796),
    'Sitakundu': (22.5657, 91.8110),
    'Rupnagar': (23.7594, 90.4081),
    'Betagi upazila': (22.4688, 90.7282),
    'Jatrabari': (23.7195, 90.4640),
    'Rangunia': (22.4988, 91.8968),
    'Haldoba': (24.5498, 88.4244),
    'Lalmonirhat': (25.9977, 89.2716),
    'Ashulia': (23.9304, 90.2538),
    'Chowdhurygachh': (23.7171, 90.5208),
    'Purbakolaujan': (24.1555, 88.7434),
    'Sultana Razia': (23.5793, 89.8248),
    'Mirzapur': (24.1604, 90.3988),
    'Chakaria': (21.7339, 91.9657),
    'Harinchara': (23.1637, 90.7861),
    'Tigerpass': (23.0080, 89.7983),
    'Mirsarai': (22.8390, 91.2396),
    'Kendua': (25.5436, 91.6435),
    'Khetmadpur': (24.9451, 88.9469),
    'Naupara': (23.4741, 91.1478),
    'Shamimabad': (24.0030, 91.2049),
    'Uttara': (23.8759, 90.3798),
    'Hatirjheel': (23.7784, 90.4048),
    'Batapukuria': (25.9519, 89.2323),
    'Akkelpur': (24.2925, 89.7253),
    'Pakundia': (23.9978, 90.7324),
    'Aditmari': (25.1392, 89.3207),
    'Begumganj': (23.1482, 90.9220),
    'Jhikra Haritala': (23.2281, 91.3832),
    'Surma': (24.3745, 91.3976),
    'Bouniabadh': (23.6177, 90.2125),
    'Kathalbaria': (22.9869, 90.7526),
    'Kamarkhanda': (24.1742, 88.9867),
    'Kadampur': (23.8433, 90.4017),
    'Brahmanbaria': (23.9575, 91.1110),
    'Mohanpur': (24.2687, 88.4441),
    'Lalpur': (24.3433, 88.6228),
    'Godagari': (24.4919, 88.9946),
    'Nabinagar of Brahmanbaria': (23.9466, 91.1469),
    'Bagura': (24.1080, 89.9805),
    'Mollah': (23.3605, 90.9036),
    'Charpara': (23.4266, 90.9559),
    'Kadamtoli': (23.7222, 90.4570),
    'Chatkhil': (23.2853, 91.0873),
    'Moksedpur': (23.4665, 90.2894),
    'Osmaninagar': (24.4267, 91.6106),
    'Kutumbapur': (23.3133, 90.7515),
    'Suhilpur': (23.6890, 89.9379),
    'Joypurhat': (25.0956, 89.0210),
    'Majidpur': (23.7988, 90.1025),
    'Karimganj': (24.0538, 90.0073),
    'Gulistan': (23.7240, 90.4075),
    'Gomastapur': (24.4907, 88.8121),
    'Narayanganj': (23.6337, 90.4966),
    'Kumarpara': (24.0181, 91.0206),
    'Bashundhara': (23.8481, 90.2596),
    'Joypura': (24.1924, 90.5438),
    'Rajkumar': (23.6662, 90.0172),
    'Chunati': (22.8253, 91.6966),
    'Mirsharai': (22.8673, 91.4421),
    'Ulail': (24.4936, 91.4914),
    'Dhulondi': (23.8643, 89.8963),
    'Kulia': (22.9104, 89.9870),
    'Sylhet': (24.8949, 91.8687),
    'Mahipur': (24.8706, 91.4632),
    'Haripur': (24.9617, 91.6577),
    'Noringpur': (24.9102, 91.8906),
    'Gazaria Upazila Bus Terminal': (23.7022, 90.3895),
    'Terminal in Gazaria Upazila South': (23.7022, 90.3895),
    'Bhaberchar Bus Terminal in Gazaria Upazila': (23.7022, 90.3895),
    'Kachua upazila': (22.9604, 90.0116),
    'Shibganj Upazila': (25.1077, 89.5059),
    'Gomostapur upazila': (25.1931, 89.4865),
    'Boglain Gomostapur upazila': (25.1931, 89.4865),
    'Shibnganj upazila': (25.9312, 89.0332),
    'Panchagarh': (26.3416, 88.5549),
    'Junaidpur': (22.8853, 89.1646),
    'Paltan': (23.7289, 90.4113),
    'Puthia': (24.4032, 88.8625),
    'Madina': (24.4336, 90.7854),
    'Bazar in Dohar upazila Phultala': (23.5931, 90.1063),
    'Sadar upazila Dulafir Majar in Sadar upazila Majar in Sadar upazila': (23.6703, 90.8865),
    'Amirpur': (23.5642, 90.3078),
    'Jointapur': (24.0159, 89.7273),
    'Jethua village': (24.3698, 88.9926),
    'Chaina': (23.0225, 89.9206),
    'Bhuapur': (24.1163, 90.1376)
}



def extract_single_dates(data):
    try:
        date_components = data.split(' ')
        month = date_components[0]
        day = date_components[1] if len(date_components) > 1 else None
            
        if month[:3].capitalize() in ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]:
            date_string = f"{day}/{month[:3].capitalize()}/2023"
            date_obj = datetime.strptime(date_string, '%d/%b/%Y')
            return date_string
        else:
            return None
    except ValueError:
        print("Error extracting date")



def read_accident_data_from_csv(file_path):
    accident_data_list = []
    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  
        for row in reader:
            row =''.join(row).split(';')
            #location = row[0].split(";")[0].strip("[]").split(",")[0].strip("'")
            location_parts = row[0].split(";")[0].strip("[]").split(",")[0]
            if "'" in location_parts:
                location = location_parts.split("'")[1]
            else:
                location = location_parts

            date_str = row[1].strip("[]'").split("' '")[0]
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

            if "[" in row[3] and "]" in row[3]:
                casualties_parts = row[3].replace("[", "").replace("]", "").split("' '")
                casualties = ", ".join([c.strip("'") for c in casualties_parts])
            else: 
                print("Unexpected format for casualties:", row[3])
                casualties = None
                continue

            if "[" in row[4] and "]" in row[4]:
                casualties_parts = row[4].replace("[", "").replace("]", "").replace("'", "").split(",")
                casualties_age = " ".join([c.strip() for c in casualties_parts])
            else:
                print("Unexpected format for casualties age:", row[4])
                casualties_age = None
                continue

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
                    casualties=casualties,
                    casualties_age=casualties_age,
                    injured= int(row[5]),
                    accident_reason=row[6],
                    action_sequence=row[7],
                    link=row[8],
                    exact_location_name = location
                )
                accident_data_list.append(accident)
            
            # for accident in accident_data_list:
            #     print(accident)

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
        self.filter_tab.setFixedWidth(300) 
        self.filter_tab.setStyleSheet("background-color: #2E5229; padding: 20px;")

        # filter_by_date_label = QLabel("Accident's Date")
        # filter_by_date_label.setAlignment(Qt.AlignCenter)
        # filter_by_date_label.setStyleSheet("color: white; font-size: 14px; font-weight: bold; margin-bottom: 0px;")
        # self.filter_layout.addWidget(filter_by_date_label, alignment=Qt.AlignCenter)
    
        date_layout = QHBoxLayout()
        self.start_date_edit = QDateEdit()
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.setFixedSize(140, 30)
        self.start_date_edit.setStyleSheet("margin-bottom: 0;")
        date_layout.addWidget(self.start_date_edit)

        self.end_date_edit = QDateEdit()
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.setFixedSize(140, 30)
        date_layout.addWidget(self.end_date_edit)
        self.filter_layout.addLayout(date_layout)

        vehicles_layout = QHBoxLayout()
        self.num_vehicles_label = QLabel("Number of Vehicles:")
        self.num_vehicles_label.setStyleSheet("color: white; font-size: 14px; font-weight: bold; margin-bottom: 0px;")
        self.num_vehicles_label.setAlignment(Qt.AlignCenter)
        vehicles_layout.addWidget(self.num_vehicles_label)

        self.num_vehicles_edit = QLineEdit()
        self.num_vehicles_edit.setFixedSize(70, 30)
        self.num_vehicles_edit.setAlignment(Qt.AlignCenter)
        vehicles_layout.addWidget(self.num_vehicles_edit)
        self.filter_layout.addLayout(vehicles_layout)

        casualties_layout = QHBoxLayout()
        self.num_casualties_label = QLabel("Number of Casualties:")
        self.num_casualties_label.setStyleSheet("color: white; font-size: 14px; font-weight: bold; margin-bottom: 0px;")
        self.num_casualties_label.setAlignment(Qt.AlignCenter)
        casualties_layout.addWidget(self.num_casualties_label)

        self.num_casualties_edit = QLineEdit()
        self.num_casualties_edit.setFixedSize(70, 30)
        self.num_casualties_edit.setAlignment(Qt.AlignCenter)
        casualties_layout.addWidget(self.num_casualties_edit)
        self.filter_layout.addLayout(casualties_layout)

        injured_layout = QHBoxLayout()
        self.num_injured_label = QLabel("Number of Injured:")
        self.num_injured_label.setStyleSheet("color: white; font-size: 14px; font-weight: bold; margin-bottom: 0px;")
        self.num_injured_label.setAlignment(Qt.AlignCenter)
        injured_layout.addWidget(self.num_injured_label)

        self.num_injured_edit = QLineEdit()
        self.num_injured_edit.setFixedSize(70, 30)
        self.num_injured_edit.setAlignment(Qt.AlignCenter)
        injured_layout.addWidget(self.num_injured_edit)
        self.filter_layout.addLayout(injured_layout)

        # link_label = QLabel("Accident's Search by Link")
        # link_label.setAlignment(Qt.AlignCenter)
        # link_label.setStyleSheet("color: white; font-size: 14px; font-weight: bold; margin-bottom: 0px;")
        # self.filter_layout.addWidget(link_label, alignment=Qt.AlignCenter)
        # self.filter_layout.setSpacing(0)

        link_layout = QHBoxLayout()
        self.link_edit = QLineEdit()
        self.link_edit.setFixedSize(150, 30)
        self.link_edit.setAlignment(Qt.AlignCenter)
        link_layout.addWidget(self.link_edit)

        self.extract_accident_button = QPushButton("Extract")
        self.extract_accident_button.clicked.connect(self.extract_accident_from_link)
        self.extract_accident_button.setStyleSheet("color: white; font-size: 10px;")
        self.extract_accident_button.setFixedSize(90, 30)
        link_layout.addWidget(self.extract_accident_button)
        self.filter_layout.addLayout(link_layout)

        self.filter_button = QPushButton("Filter")
        self.filter_button.clicked.connect(self.filter_accidents)
        self.filter_layout.addWidget(self.filter_button)

        self.clear_filter_button = QPushButton("Clear")
        self.clear_filter_button.clicked.connect(self.clear_filters)
        self.filter_layout.addWidget(self.clear_filter_button)

        self.layout.addWidget(self.filter_tab)

        self.map_widget = QWebEngineView()
        self.map_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  
        self.layout.addWidget(self.map_widget)
        self.map_widget.setHtml(self.generate_html())

        self.toolbar = self.addToolBar("Toolbar")
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.goBack)
        self.toolbar.addWidget(self.back_button)

        self.browser = QWebEngineView()
        self.layout.addWidget(self.browser)
        self.generate_html()
    

    def extract_accident_from_link(self):
        link_text = self.link_edit.text()
        found_accidents = []
        for accident in self.accident_data_list:
            if accident.link == link_text:
                found_accidents.append(accident)
        if found_accidents:
            self.filtered_accidents = found_accidents
            self.map_widget.setHtml(self.generate_html())
        else:
            print("Accident not found for link:", link_text)

    def filter_accidents(self):
        start_date_qdate = self.start_date_edit.date()
        end_date_qdate = self.end_date_edit.date()
        

        if start_date_qdate == end_date_qdate and start_date_qdate.toString("dd/MMM/yyyy") == "01/Jan/2000":
            start_date = None
            end_date = None
        else:
            start_date_str = start_date_qdate.toString("dd/MMM/yyyy")
            end_date_str = end_date_qdate.toString("dd/MMM/yyyy")
            start_date = datetime.strptime(start_date_str, "%d/%b/%Y")
            end_date = datetime.strptime(end_date_str, "%d/%b/%Y")


        # debugging print statements
        print(f"Start Date: {start_date}")
        print(f"End Date: {end_date}")
        
        num_vehicles_text = self.num_vehicles_edit.text().strip()
        num_casualties_text = self.num_casualties_edit.text().strip()
        num_injured_text = self.num_injured_edit.text().strip()
        
        num_vehicles = int(num_vehicles_text) if num_vehicles_text else None
        num_casualties = int(num_casualties_text) if num_casualties_text else None
        num_injured = int(num_injured_text) if num_injured_text else None

        print(f"Number of Vehicles: {num_vehicles}")
        print(f"Number of Casualties: {num_casualties}")
        print(f"Number of Injured: {num_injured}")


        filtered_accidents = []
        for accident in self.accident_data_list:
            try:
                accident_date = datetime.strptime(accident.date, "%d/%b/%Y")
            except ValueError as e:
                print(f"Date format error for accident: {accident.date}, error: {e}")
                continue
            date_criteria = start_date <= accident_date <= end_date if start_date and end_date else True

            vehicles_criteria = num_vehicles is None or (len(accident.vehicles.split(' ')) if len(accident.vehicles.split(' ')) > 1 else 1) == num_vehicles
            casualties_criteria = num_casualties is None or (len(accident.casualties.split(',')) if ',' in accident.casualties else 0) == num_casualties
            injured_criteria = num_injured is None or (accident.injured is not None and accident.injured == num_injured)

            print(f"Accident Date: {accident_date}")
            print(f"Vehicles Criteria: {vehicles_criteria}")
            print(f"Casualties Criteria: {casualties_criteria}")
            print(f"Injured Criteria: {injured_criteria}")
            
            if date_criteria and vehicles_criteria and casualties_criteria and injured_criteria:
                filtered_accidents.append(accident)

        print(f"Filtered Accidents: {filtered_accidents}")

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
                    .bindPopup('<b>Accident:</b><br>Location: {accident.exact_location_name}<br>Date: {accident.date}<br>Vehicles: {accident.vehicles}<br>Casualties: {accident.casualties}<br>Casualties Age: {accident.casualties_age}<br>Injured: {accident.injured}<br>Reason: {accident.accident_reason}<br>Action: {accident.action_sequence}<br><a href="{accident.link} ">More info</a>')
                    .openPopup();
            """

        html += """
            </script>
        </body>
        </html>
        """
        return html
    
    
    def goBack(self):
        self.filtered_accidents = self.accident_data_list.copy()
        self.map_widget.setHtml(self.generate_html())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    accident_data_list = read_accident_data_from_csv("processed_events2.csv")

    window = MapWindow(accident_data_list)
    window.show()
    sys.exit(app.exec())

