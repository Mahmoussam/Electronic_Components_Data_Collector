from Pcraper.dcrapers.dwolfspeed import *
from Pcraper.data_writers.CSVWriter import CSVWriter
import logging
import requests
from io import BytesIO

logging.basicConfig(
        level=logging.INFO )
logger = logging.getLogger(__name__)

url = "https://assets.wolfspeed.com/uploads/2024/01/Wolfspeed_E4M0013120K_data_sheet.pdf"#"https://cms.wolfspeed.com/download/58104"
res = requests.get(url)

print("Status code : ",res.status_code)

pdf = BytesIO(res.content)

dsws = DSWolfSpeedMOS()
with CSVWriter('C3M0045065D.csv' , delimiter = ';') as writer:
    dsws.scrap(pdf , writer)

"""
import camelot

# Read pages 1–2
tables_lattice = camelot.read_pdf("datasheet.pdf", pages="1-3", flavor="lattice")
#tables_stream  = camelot.read_pdf("datasheet.pdf", pages="1-2", flavor="stream")

# Convert to plain lists and concatenate
all_tables = list(tables_lattice) #+ list(tables_stream)

for i, table in enumerate(all_tables, start=1):
    print(f"\n--- Table #{i} (extract from {table.page} flavor={table.flavor}) ---")
    print(table.df)

# Export the first two lattice tables:
if len(tables_lattice) >= 2:
    tables_lattice[0].to_csv("key_parameters.csv", index=False, encoding="utf-8")
    tables_lattice[1].to_csv("electrical_characteristics.csv", index=False, encoding="utf-8")
"""
