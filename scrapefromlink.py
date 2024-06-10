import processing
import scrapers
import classes
import acquisition

def scrape_from_scratch(link):
    meta_data = scrapers.scrape_metadata(link)
    processing.process_and_save(meta_data, 'processed_events.csv')

links=["https://www.unb.com.bd/category/Bangladesh/man-killed-in-kushtia-road-crash/4366"]

scrape_from_scratch(links)

