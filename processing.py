# imports needed for this project
import os
import time
import pandas as pd
import spacy
from spacy.matcher import Matcher
from classes import AccidentData, MetaData
from scrapers import read_links_from_file, scrape_metadata, write_metadata_to_csv
import re
from transformers import pipeline

# loading spaCy model
nlp = spacy.load('en_core_web_sm')
matcher = Matcher(nlp.vocab)

# Hugging Face zero-shot classification pipeline initzialization
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")


# vehicle type dictionary
vehicle_mapping = {
    "bus": "Bus", "car": "Car", "noah": "Noah", "human hauler": "Human hauler",
    "trolley": "Trolley", "chander gari": "Chander Gari", "auto rickshaw": "Auto Rickshaw",
    "cng": "CNG", "easy-bike": "Easy-bike", "truck": "Truck", "garbage truck": "Garbage Truck",
    "trailer": "Trailer", "motorcycle": "Motorcycle", "microbus": "Microbus", "scooter": "Scooter",
    "construction vehicle": "Construction vehicle", "bicycle": "Bicycle", "ambulance": "Ambulance",
    "pickup": "Pickup", "lorry": "Lorry", "paddy cutter vehicles": "Paddy cutter vehicles",
    "bulkhead": "Bulkhead", "crane": "Crane", "wrecker": "Wrecker", "tractor": "Tractor",
    "cart": "Cart", "leguna": "Leguna", "nosimon": "Nosimon", "three-wheeler": "Three-Wheeler",
    "four-wheeler": "Four-Wheeler", "votvoti": "Votvoti", "kariman": "Kariman", "mahindra": "Mahindra",
    "van": "Van", "rickshaw": "Rickshaw", "boat": "Boat", "trawler": "Trawler", "vessel": "Vessel",
    "launch": "Launch", "tanker": "Tanker", "oil tanker": "Oil Tanker", "road roller": "Road roller",
    "power tiller": "Power Tiller", "excavator": "Excavator", "train": "Train", "airplane": "Airplane",
    "pedestrian": "Pedestrian"
}

# function created for mapping vehicle names to their standard forms
def map_vehicle_names(vehicles):
    mapped_vehicles = []
    for vehicle in vehicles:
        vehicle_lower = vehicle.lower().strip()
        if vehicle_lower in vehicle_mapping:
            mapped_vehicles.append(vehicle_mapping[vehicle_lower])
        else:
            mapped_vehicles.append("Other")  # or use "Unknown" or "Null" if preferred
    return list(set(mapped_vehicles))  # removing duplicates


# function created for cleaning and deduplicating lists
def clean_and_deduplicate(items):
    seen = set()
    cleaned = []
    for item in items:
        singular = item.lower().rstrip('s')
        if singular not in seen:
            seen.add(singular)
            cleaned.append(item)  # just to keep the original form
    return cleaned

# function created for removing duplicates and filtering non-Bangladeshi locations
def clean_locations(locations):
    cleaned = []
    for loc in locations:
        if loc not in cleaned and loc != 'Saudi Arabia' and loc != 'UAE':
            cleaned.append(loc)
    return cleaned

# function created for cleaning and deduplicating dates and removing ages
def clean_dates(dates):
    cleaned = []
    for date in dates:
        if not date.isdigit():  # for check - if the date is purely numeric or not
            cleaned.append(date)
    return list(dict.fromkeys(cleaned))

#simple function to get rid of duplicates using set
def remove_duplicates_simple(text_list):
    return list(set(text_list))

#More advanced function for removing duplicates which takes into account substrings
def remove_shorter_duplicates(names):
    sorted_names = sorted(names, key=len, reverse=True)  
    final_names = []

    for name in sorted_names:
        if not any(name in existing_name for existing_name in final_names if existing_name != name):
            final_names.append(name)

    return final_names

#Second version of the function above 
def remove_shorter_duplicates2(name_set):
    names = list(name_set)
    to_remove = set()

    for i in range(len(names)):
        for j in range(len(names)):
            if i != j:
                if names[i] in names[j] and len(names[i]) < len(names[j]):
                    to_remove.add(names[i])
                elif names[j] in names[i] and len(names[j]) < len(names[i]):
                    to_remove.add(names[j])

    cleaned_set = set(names) - to_remove  
    return list(cleaned_set)  


#Third version of the remove_duplicates but it's the same as first one
def remove_substrings(phrases):
    # Sort phrases by length in descending order
    sorted_phrases = sorted(phrases, key=len, reverse=True)
    longest_phrases = []

    for phrase in sorted_phrases:
        if not any(phrase in other for other in longest_phrases if phrase != other):
            longest_phrases.append(phrase)

    return longest_phrases

#function to set up matcher for injured people
def setup_injured_matcher(matcher):
    pattern = [
        {"LIKE_NUM": True},
        {"LOWER": "more", "OP": "?"},
        {"LOWER": "people", "OP": "?"},
        {"LEMMA": {"IN": ["injure", "hurt"]}},
        {"POS": "ADP", "OP": "?"},
        {"IS_ALPHA": True, "OP": "*"}
    ]
    matcher.add("INJURED_COUNT", [pattern])
    return matcher

#function to set up matcher for upazila extraction
def setup_upazila_matcher(matcher):
        # Pattern 1: "Location in Location upazila"
    pattern1 = [
        {"POS": "PROPN", "OP": "+"},  
        {"LOWER": "in"},              
        {"POS": "PROPN", "OP": "+"},  
        {"LOWER": "upazila"}          
    ]

    # Pattern 2: "Location upazila"
    pattern2 = [
        {"POS": "PROPN", "OP": "+"},  
        {"LOWER": "upazila"}          
    ]

    # Pattern 3: "Location, upazila"
    pattern3 = [
        {"POS": "PROPN", "OP": "+"},  
        {"IS_PUNCT": True, "OP": "?"},  
        {"LOWER": "upazila"}          
    ]

    matcher.add("LocationInLocationUpazila", [pattern1, pattern2, pattern3])

    return matcher


#function to set up fatalities matcher
def setup_fatalities_matcher(nlp):
    matcher = Matcher(nlp.vocab)
    
    # Pattern for "FirstName LastName, age"
    pattern1 = [
        {"POS": "PROPN"},           
        {"IS_PUNCT": True, "OP": "?"},  
        {"POS": "PROPN"},           
        {"IS_PUNCT": True, "TEXT": ","}, 
        {"POS": "NUM"}              
    ]

    # Pattern for "FirstName, age"
    pattern2 = [
        {"POS": "PROPN"},           
        {"IS_PUNCT": True, "TEXT": ","}, 
        {"POS": "NUM"}              
    ]

    matcher.add("NameAgePattern", [pattern1, pattern2])

    return matcher



# function created for extracting casualties
def extract_casualties(doc):
    casualties = []
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            casualties.append(ent.text)
    return clean_and_deduplicate(casualties)


# function created for extracting ages
def extract_ages(doc):
    ages = []
    for ent in doc.ents:
        if ent.label_ == "DATE" and ent.text.isdigit() and 1 <= len(ent.text) <= 2:
            ages.append(ent.text)
    return list(set(ages))  


# function created for extracting injured persons
def extract_location(doc):
    locations = []
    # pattern for "number of people INJURED" phrases or similar one 
    upazila_pattern = [
    {"POS": "PROPN", "OP": "+"},  
    {"LOWER": "in"},              
    {"POS": "PROPN", "OP": "+"},  
    {"LOWER": "upazila"}          
]
    # Adding patterns to the matcher
    matcher_upazila = Matcher(nlp.vocab)
    matcher_upazila = setup_upazila_matcher(matcher_upazila)

    matches = matcher_upazila(doc)
    for match_id, start, end in matches:
        span = doc[start:end]
        locations.append(span)
    return locations
        

# function created for extracting reason for the accident using zero-shot classification
def extract_reason_hf(text):
    candidate_labels = [
      "reckless driving", "mechanical failure", "weather conditions", "driver fatigue",
      "drunk driving", "overspeeding", "road conditions", "pedestrian error",
      "animal crossing", "poor lighting", "distracted driving", "traffic signal violation",
      "tailgating", "sudden braking", "illegal overtaking", "vehicle defects",
      "road construction", "failure to yield", "aggressive driving", "inexperienced driver",
      "running a red light", "improper lane changing", "speeding in work zones",
      "driver inattention", "dangerous intersections", "vehicle overloading", "drowsy driving",
      "road debris", "icy roads", "fog", "heavy rain", "snow", "hail", "strong winds", "glare",
      "potholes", "poor road maintenance", "swerving to avoid obstacles", "brake failure",
      "tire blowout", "steering failure", "engine failure", "transmission failure",
      "exhaust system failure", "electrical system failure", "defective headlights",
      "defective brake lights", "faulty windshield wipers", "malfunctioning turn signals",
      "distracted pedestrians", "jaywalking", "crossing against the signal", "walking in the roadway",
      "intoxicated pedestrians", "bicycle accidents", "motorcycle accidents", "truck accidents",
      "bus accidents", "construction vehicle accidents", "farming equipment accidents",
      "emergency vehicle accidents", "hit and run", "driver medical emergency", "road rage",
      "failing to check blind spots", "using a mobile phone", "eating while driving",
      "adjusting the radio", "talking to passengers", "reaching for objects", "texting while driving",
      "smoking while driving", "unsecured cargo", "failure to signal", "sudden lane departure",
      "intersection accidents", "rear-end collisions", "side-impact collisions", "head-on collisions",
      "single-vehicle crashes", "multi-vehicle pileups", "parking lot accidents", "reversing accidents",
      "bicycle collisions", "school zone accidents", "animal-vehicle collisions", "rollover accidents",
      "T-intersection accidents", "U-turn accidents", "roundabout accidents", "traffic congestion",
      "overcrowded vehicles", "negligent driving", "speeding in residential areas", "unfamiliar roads",
      "wildlife crossings", "poor signage", "confusing road layout", "unfamiliar vehicle",
      "driver inexperience with road conditions"
    ]
    if len(text) > 512:
        text = text[:512]
    results = classifier(text, candidate_labels)
    top_reason = results['labels'][0]
    return top_reason


# function created for extracting sequence of actions using SpaCy (and remove duplicates also)
def extract_sequence_of_actions_spacy(doc):
    actions = []
    for sent in doc.sents:
        for token in sent:
            if token.dep_ in ('nsubj', 'ROOT', 'dobj') and token.pos_ == 'VERB':
                actions.append(token.text)
    actions = list(dict.fromkeys(actions))  
    return ' '.join(actions)
    

#
def extract_fatalities(doc, matcher):
    death_related_terms = ['killed', 'deceased', 'succumbed', 'died', 'fatalities']
    fatality_context = False
    potential_victims = []
    actual_fatalities = []

    for sent in doc.sents:
        matches = matcher(sent)
        for match_id, start, end in matches:
            potential_victims.append(sent[start:end-2].text)  

        if any(death_term in sent.text.lower() for death_term in death_related_terms):
            fatality_context = True
            actual_fatalities.extend(potential_victims)
            potential_victims = []  
        else:
            fatality_context = False

    return remove_shorter_duplicates(actual_fatalities)



def extract_injured(doc):
    injured_count = 0
    matcher_injured = Matcher(nlp.vocab)
    matcher_injured = setup_injured_matcher(matcher_injured)
    matches = matcher_injured(doc)
    phrases = []

    # Collect all matched phrases
    for match_id, start, end in matches:
        phrase = doc[start:end].text
        phrases.append(phrase)

    # Remove substrings
    longest_phrases = remove_substrings(phrases)

    # Process each unique longest phrase to sum up injured counts
    for phrase in longest_phrases:
        match = re.search(r'\d+|one|two|three|four|five|six|seven|eight|nine|ten', phrase, re.IGNORECASE)
        if match:
            num_word = match.group().lower()
            num_dict = {
                "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
                "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10
            }
            count = num_dict.get(num_word, 0) if num_word in num_dict else int(num_word)
            injured_count += count

    return injured_count



def extract_fatal_names(doc):
    death_related_terms = ['killed', 'deceased', 'succumbed', 'died', 'fatalities']
    fatal_names = set()  

    for sent in doc.sents:
        if any(term in sent.text.lower() for term in death_related_terms):
            for ent in sent.ents:
                if ent.label_ == 'PERSON':
                    fatal_names.add(ent.text)

    return list(fatal_names)
    

# function created for extracting details
def extract_details(meta_data_list):
    processed_data = []

    for text in meta_data_list:
        doc = nlp(str(text.raw_text))

        # location
        locations = [ent.text for ent in doc.ents if ent.label_ == 'GPE']
        locations = clean_locations(locations)
        exact_locations = extract_location(doc)
        exact_locations = remove_shorter_duplicates2(exact_locations)

        if not locations:
            locations = exact_locations
        
        #Extract date, find day of the week etc.
        date_info = [ent.text for ent in doc.ents if ent.label_ == 'DATE' or ent.label_ == 'TIME']
        date_info = clean_dates(date_info)

        # vehicles
        matcher_vechicles = Matcher(nlp.vocab)
        # adding vehicle pattern to matcher
        vehicle_patterns = [[{"LEMMA": {"IN": list(vehicle_mapping.keys())}}]]
        matcher_vechicles.add("VEHICLE_TYPE", vehicle_patterns)
        matches = matcher_vechicles(doc)
        vehicles = [doc[start:end].text for match_id, start, end in matches]
        vehicles = map_vehicle_names(clean_and_deduplicate(vehicles))

        # casualties 
        casualties = extract_fatalities(doc, setup_fatalities_matcher(nlp))

        if not casualties:
            casualties += extract_fatal_names(doc)
        # number of injured persons
        injured = extract_injured(doc)

        # reason for the accident
        #reason = extract_reason_hf(text.raw_text)

        # sequence of actions
        #actions = extract_sequence_of_actions_spacy(doc)

        # AccidentData object
        accident_data = AccidentData(
            location= locations,
            date= date_info,
            vehicles= vehicles,
            casualties= casualties,
            casualties_age= extract_ages(doc),
            injured= injured,
            accident_reason= "null",
            action_sequence= "null",
            link= text.link,
            exact_location_name = exact_locations
        )

        processed_data.append(vars(accident_data))

    return processed_data


def process_and_save(meta_data_list, output_file):
    processed_data = extract_details(meta_data_list)
    df = pd.DataFrame(processed_data)
    df.to_csv(output_file, sep=';', index=False)