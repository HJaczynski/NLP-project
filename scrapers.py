from bs4 import BeautifulSoup
from classes import AccidentData, MetaData
import requests
import re
import time
from datetime import datetime
import csv

# Function to extract the date from a string using regular expressions
def extract_date_from_string(text):
    # Regular expression pattern to match the date format
    pattern = r'([A-Za-z]+ \d{1,2}, \d{4}, \d{2}:\d{2} [AP]M)'
    
    match = re.search(pattern, text)
    
    if match:
        date = match.group(1)
        return date
    else:
        return None


# Function to obtain the links to scrape from the UNB API
def fetch_unb_api():
    api_id = 0
    has_more = True
    links_to_scrape = set()

    keywords = ["road-crash", "road", "highwawy", "vehicle", 
                "car", "truck", "bus", "motorcycle", "collision", 
                "accident", "human-hauler"]

    while has_more is True:
        http_link = f"https://www.unb.com.bd/api/tag-news?tag_id=54&item={api_id}"
        response = requests.get(http_link)
        data = response.json()
        has_more = data['hasMore']
        html_content = data['html']
        soup = BeautifulSoup(html_content, 'lxml')

        for anchor in soup.find_all('a', href=True):
            for keyword in keywords:
                href = anchor.get('href')
                if keyword in anchor['href'] and href.startswith('https://www.unb.com.bd/category/Bangladesh/'):
                    links_to_scrape.add(anchor['href'])

        
        print(f"[{api_id}]: {has_more}")
        api_id += 1
        time.sleep(1)
        
    return list(links_to_scrape)


# Function to scrape the UNB articles for metadata
def scrape_metadata(links):
    meta_data_list = []

    for link in links:
        title = ""
        raw_text = ""
        update_date = None

        print(f"Scrapping [{link}]")

        html_text = requests.get(link)
        soup = BeautifulSoup(html_text.text, 'lxml')

        information = soup.find_all('li', class_='news-section-bar')
        html_raw_text= soup.find_all('div', class_="news-article-text-block text-patter-edit ref-link")

        #As html_raw_text info has < and > we want to get rid of it as it destroys our csv parsing. We could drop them but I found out one can use this lt and gt (less/greater than)
        cleaned_text_list = []
        for html_element in html_raw_text:
            element_string = str(html_element)
            cleaned_string = element_string.replace('<', '&lt').replace('>', '&gt')
            cleaned_text_list.append(cleaned_string)

        html_raw_text = cleaned_text_list

        if len(information) > 4:
            meta_location = information[0].text
        else:
            meta_location = "Bangladesh"

        # Extract the publication and update date
        for info in information:
            if "Publish" in info.text:
                date_str = extract_date_from_string(info.text)
                publication_date = datetime.strptime(date_str, '%B %d, %Y, %I:%M %p')
            elif "Update" in info.text:
                date_str = extract_date_from_string(info.text)
                update_date = datetime.strptime(date_str, '%B %d, %Y, %I:%M %p')
                break


        # Extract the title of the article
        title_div = soup.find('div', class_='upper-box')
        if title_div:
            h2_tag = title_div.find('h2')
            if h2_tag:
                title = h2_tag.text.rstrip()

        # Extract the raw text from the article
        divs = soup.find_all('div', class_='text')
        for div in divs:
            raw_text += div.get_text(separator=" ", strip=True)
            
        
        # Create a new MetaData object and append it to the list
        new_md = MetaData(publication_date, update_date, meta_location, title, html_raw_text, raw_text, link)
        meta_data_list.append(new_md)

    # Return the list of MetaData objects
    return meta_data_list


# This does not work, needs fixing in the future
def write_metadata_to_csv(meta_data_list, filename):
    with open(f"{filename}.csv", "w", encoding="utf-8") as f:
        f.write("<Title>;<Publication Date>;<Update Date>;<Location>;<Link>;<Raw Text>;<HTML Text>\n")
        for md in meta_data_list:
            f.write(f"<{md.title}>;<{md.publication_date}>;<{md.update_date}>;<{md.meta_location}>;<{md.link}>;\"<{md.raw_text}>\";<{md.HTML_text}>\n")
    print("Metadata written to file.")


# This does not work, needs fixing in the future
def write_raw_text_to_csv(meta_data_list, filename):
    with open(f"{filename}.csv", "w", encoding="utf-8") as f:
        f.write("<Raw Text>\n")
        for md in meta_data_list:
            f.write(f"{md.raw_text}")
    print("Metadata written to file.")

def read_metadata_from_csv(filename):
    meta_data_list = []

    with open(f"{filename}.csv", "r", encoding="utf-8") as f:
        csv_reader = csv.reader(f, delimiter=';')
        next(csv_reader)  # Skip the header row

        for row in csv_reader:
            # Create an instance of MetaData for each row
            metadata = MetaData(
                publication_date=row[1],
                update_date=row[2],
                meta_location=row[3],
                title=row[0],
                html_text=row[6],
                raw_text=row[5],
                link=row[4]
            )
            meta_data_list.append(metadata)
    
    return meta_data_list

# Function to write the links obtained from the UNB API to a txt file
def write_links_to_file(links):
    f = open("links.txt", "w")
    for link in links:
        f.write(link + "\n")
    f.close()
    print("Links written to file.")


# Function to read the links from a txt file
def read_links_from_file(filename):
    links = []
    f = open(filename, "r")
    for line in f:
        links.append(line.strip())
    f.close()
    return links