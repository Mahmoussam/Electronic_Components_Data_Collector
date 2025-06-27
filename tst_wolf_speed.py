from Pcraper.scrapers.common_imports import *
from Pcraper.scrapers import wolfspeed
from Pcraper.data_writers.CSVWriter import CSVWriter
from Pcraper.dcrapers.dwolfspeed import *

import logging
import requests
from io import BytesIO
import json
import os

if __name__ == '__main__':
        
    url = "https://www.wolfspeed.com/products/power/sic-mosfets/"
    SAVE_DOCS_ON_DISK = True  # enabled to save the requested documents on disk too
    COOKIE_FILE = "cookies.json"
    

    logging.basicConfig(
        level=logging.INFO )
    logger = logging.getLogger(__name__)

    ## init driver and its cookies:
    
        
    service = Service("chromedriver-win64/chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    driver.get(url)
    # load cookies from file
    if os.path.exists(COOKIE_FILE):
        with open(COOKIE_FILE, "r", encoding="utf-8") as f:
            cookies = json.load(f)

        for cookie in cookies:
            # Selenium expects expiry as int, not float or None
            if "expiry" in cookie:
                cookie["expiry"] = int(cookie["expiry"])
            driver.add_cookie(cookie)
            
    dsws = DSWolfSpeedMOS()
    ws = wolfspeed.WolfSpeed()
    logging.info('Scrapping web table:')
    with CSVWriter('sic_mosfets.csv' , delimiter = ';') as writer:
        ds_links = ws.scrap_data(driver , url , writer)
    ## re-use cookies to evade the accept cookies button..
    cookies = driver.get_cookies()  
    with open(COOKIE_FILE, "w", encoding="utf-8") as f:
        json.dump(cookies, f, ensure_ascii=False, indent=2)
    
    driver.close()
    logging.info('Scraping docs!')
    for [mosfet , url] in ds_links:
        if url is None:
            logging.info("No url to request doc %s" , mosfet)
            continue
        res = requests.get(url)
        if res.status_code != 200:
            logger.info("Failed to request %s , status_code = %d" , mosfet , res.status_code)
            continue
        if SAVE_DOCS_ON_DISK:
            with open('data_sheets/'+mosfet+'.pdf','wb') as pdf:
                pdf.write(res.content)
        try:
            pdf = BytesIO(res.content)
            with CSVWriter('data_sheets/'+mosfet+'.csv' , delimiter = ';') as writer:
                dsws.scrap(pdf , writer)
        except:
            logger.exception("Failed to parse document %s" , mosfet)
        
