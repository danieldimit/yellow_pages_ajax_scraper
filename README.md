# Yellowpages (Gelbeseiten) scraper
A tool made for scraping gelbeseiten.de in 2022. Data is being scraped from ajax infinite scroll POST requests.

## Running the tool

The tool was tested with python 3.8 and scrapy.

To install scrapy do:
```
pip install scrapy
```

To run the program do:
```
scrapy runspider scraper.py
```

## Output

The program output a csv file with extracted yellow pages entries - addresses, names, phones and emails