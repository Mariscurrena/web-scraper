import requests
from bs4 import BeautifulSoup
from datetime import datetime

#url = 'https://www.amazon.com.mx/dp/B0F5WRWBPZ/ref=sspa_dk_detail_0?psc=1&pd_rd_i=B0F5WRWBPZ&pd_rd_w=NvgkX&content-id=amzn1.sym.98349eff-970d-4329-9808-569eb2fa7330&pf_rd_p=98349eff-970d-4329-9808-569eb2fa7330&pf_rd_r=K40HC2A0FVTZHSBSRSGM&pd_rd_wg=z2npJ&pd_rd_r=4b67b796-1eb0-468d-989c-24a9e87c25da&sp_csd=d2lkZ2V0TmFtZT1zcF9kZXRhaWw'
url = 'https://www.amazon.com.mx/SAMSUNG-Auriculares-inal%C3%A1mbricos-optimizaci%C3%B3n-latinoamericana/dp/B0D9C8VNSN/ref=sr_1_6?crid=3KMKGLOR7J7VA&dib=eyJ2IjoiMSJ9.aoGYhsLA7yEChavQ-qRukRdNeIcu9Chgqy29t-453gYosMR-WKpN7CqKDDC-lO8p1DqqRE9wsC9hjv2N4mncn8YVAJTHObav_48dUeHVQS7Ilf_BsNUj1ad2w8qnsiw8-LpVOGOlejik-yPOagIBMzGI9o6fnxQw5kEMYPBYG6IPXv5tPWnMr2cmXyuHfrrn4MTNXIM65euKVMgmnhkk8wxozGABrJcqClQJ5zRoSWSNi1Oj5NbHccQQnnd9Oph9x2PBJOohH2qIj99yhNvOcY48dWf2kI6-3gAkcCKCfdM.Q1sWrzObEL6fEQ7l7JiKndcwfIzXyW-Q5zDiHKHLBHg&dib_tag=se&keywords=galaxy%2Bbuds%2B3%2Bpro&qid=1750705956&sprefix=galaxy%2Bbu%2Caps%2C115&sr=8-6&ufe=app_do%3Aamzn1.fos.628a2120-cf12-4882-b7cf-30e681beb181&th=1'
response = requests.get(url)

class colors():
    blue = "\033[34m"
    green = "\033[32m"
    orange = "\033[38;5;208m"
    red = "\033[31m"
    purple = "\033[35m"
    end = "\033[0m"

def main():
    validation()

def validation():
    if response.status_code == 200:
        print(f"{colors.green}---> Resource Available{colors.end}")
        scraping()
    else:
        print(f"{colors.red}ERROR {response.status_code}{colors.end}")
        print(f"{colors.red}---> Resource unreachable{colors.end}")

def scraping():
    soup = BeautifulSoup(response.text, 'html.parser')
    prices = soup.find_all('span', class_="a-price-whole")
    values = []
    for price in prices:
        value = price.contents[0].strip()
        values.append(value)
    
    price_saving(values[0])
    file_saving(values[0])

def file_saving(buds):
    with open('buds_price.txt' , 'a', encoding='utf-8') as file:
        file.write(f"{datetime.now()}, price is: {buds}\n")

def price_saving(buds):
    with open('buds_price.txt', 'r', encoding='utf-8') as file:
        logs = file.readlines()
    last_log = logs[-1].strip()
    buds_last_price = last_log.split('price is: ')[1].strip()
    print(f"{colors.purple}Galaxy Buds 3 Pro last price was: ${buds_last_price}{colors.purple}")
    price_validation(buds, buds_last_price)

def price_validation(buds_concurrent_price, buds_last):
    if buds_concurrent_price == buds_last:
        print (f"{colors.blue} ----------------> Price: ${buds_concurrent_price} <---------------- {colors.end}")
        print(f"{colors.blue} ---> The price is the same since the last request. {colors.end}")
    elif buds_concurrent_price < buds_last:
        print (f"{colors.orange} ----------------> Price: ${buds_concurrent_price} <---------------- {colors.end}")
        print (f"{colors.orange} ---> The price is ${to_int(buds_concurrent_price)-to_int(buds_last)} more expensive than last request. {colors.end}")
    elif buds_concurrent_price > buds_last:
        print (f"{colors.green} ----------------> Price: ${buds_concurrent_price} <---------------- {colors.end}")
        print (f"{colors.green} ---> The price is ${to_int(buds_last)-to_int(buds_concurrent_price)} cheaper than last request. {colors.end}")
    else:
        print(f"{colors.red}XXXXX UNKNOWN CONDITION. INTERNAL ERROR XXXXX{colors.end}")

def to_int(num_str):
    return int(num_str.replace(',', ''))

if __name__ == "__main__":
    main()