import requests, time, os
from bs4 import BeautifulSoup
from datetime import datetime
from pyfiglet import Figlet
from pathlib import Path

class colors():
    blue = "\033[34m"
    green = "\033[32m"
    orange = "\033[38;5;208m"
    red = "\033[31m"
    purple = "\033[35m"
    end = "\033[0m"

def main():
    title()
    time.sleep(1)
    response = requests.get(url_initialize())
    validation(response)

def url_initialize():
    url = input(f'{colors.purple}Insert the Amazon product URL:{colors.end} ')
    return url

def validation(response):
    if response.status_code == 200:
        print(f"{colors.green}\n ---> Resource Available{colors.end}")
        scraping(response)
    else:
        print(f"{colors.red}ERROR {response.status_code}{colors.end}")
        print(f"{colors.red} ---> Resource unreachable{colors.end}")

def scraping(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    prices = soup.find_all('span', class_="a-price-whole")
    values = []
    for price in prices:
        value = price.contents[0].strip()
        values.append(value)
    price_saving(values[0], soup)

def price_saving(buds, soup):
    ### if the log price file do not exist the conditional will initialize the array as zero
    if not Path("amazon_prices_logs.txt").exists():
        logs = []
    ### If exist, the log array would save all the logs into it.
    else:
        with open('amazon_prices_logs.txt', 'r', encoding='utf-8') as file:
            logs = [line.strip() for line in file if line.strip()] ### Comprehensive bucle function
    ### This saves the new log, making effective to consult the previous one, before saving a new one that would affect the validation conditions
    file_saving(buds)
    ### Sleep time to be able to perform all the tasks
    time.sleep(0.01)
    ### If log array is empty, shows a warning and take as reference the current price.
    if len(logs) == 0:
        print(f"{colors.orange} ---> No previous price found. This is the first entry.{colors.end}")
        buds_last_price = buds
    ### If array is not empty, use the last log for validation.
    else:
        last_log = logs[-1]
        buds_last_price = last_log.split('price is: ')[1].strip()

    print(f"{colors.purple} ---> {name_scraping(soup)} last price was: ${buds_last_price}{colors.end}")
    price_validation(buds, buds_last_price)


def file_saving(buds):
    prices_logs = Path("amazon_prices_logs.txt")
    prices_logs.touch(exist_ok=True)
    with open('amazon_prices_logs.txt', 'a', encoding='utf-8') as file:
        file.write(f"{datetime.now()}, price is: {buds}\n")
        file.flush()

def name_scraping(soup):
    name = soup.find('span', {'id': 'productTitle'}).get_text(strip=True)
    return name

def price_validation(buds_concurrent_price, buds_last):
    current_price_int = to_int(buds_concurrent_price)
    last_price_int = to_int(buds_last)

    if current_price_int == last_price_int:
        print(f"{colors.blue} ----------------> Price: ${buds_concurrent_price} <---------------- {colors.end}")
        print(f"{colors.blue} ---> The price is the same since the last request. {colors.end}")
    elif current_price_int < last_price_int:
        diff = last_price_int - current_price_int
        print(f"{colors.green} ----------------> Price: ${buds_concurrent_price} <---------------- {colors.end}")
        print(f"{colors.green} ---> The price is ${diff} cheaper than last request. {colors.end}")
    elif current_price_int > last_price_int:
        diff = current_price_int - last_price_int
        print(f"{colors.orange} ----------------> Price: ${buds_concurrent_price} <---------------- {colors.end}")
        print(f"{colors.orange} ---> The price is ${diff} more expensive than last request. {colors.end}")
    else:
        print(f"{colors.red}XXXXX UNKNOWN CONDITION. INTERNAL ERROR XXXXX{colors.end}")

def to_int(num_str):
    return int(num_str.replace(',', ''))

def title():
    figlet = Figlet(font='standard')
    ascii_banner = figlet.renderText('SCRAPER')
    print(f"{colors.purple}{ascii_banner}{colors.end}")
    print(f"{colors.purple} ---> SCRAPER – Web Data Extractor developed by Steve{colors.end}")

if __name__ == "__main__":
    main()