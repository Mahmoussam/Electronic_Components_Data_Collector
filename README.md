pretty poor README to be updated soon
# Basic info:
intended for py3.11
packages: [installed via pip]
  -  selenium
  -  camelot-py[cv]
  -  ghostscript ,required by camelot
# How to use?
main script is tst_wolf_speed.py , it expects a directory looking like so:
```
working Dir/
  -Pcraper/...
  -data_sheets/...
  -chromedriver-win64/
    -chromedriver.exe
  -tst_wolf_speed.py
```
Suitable chrome webdriver can be downloaded through [here](https://googlechromelabs.github.io/chrome-for-testing/) 

# Ouput:
a csv file of all components would be generated within working dir with basic info
detailed csv file for each components is generated within `data_sheets/` directory , also there is an option for saving the processed PDF (enabled by default)
