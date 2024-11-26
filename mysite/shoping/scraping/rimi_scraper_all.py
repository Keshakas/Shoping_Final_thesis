import requests
from bs4 import BeautifulSoup
import csv
import concurrent.futures

# URL sąrašas
urls = [
    "https://www.rimi.lt/e-parduotuve/lt/produktai/vaisiai-darzoves-ir-geles/c/SH-15",
    "https://www.rimi.lt/e-parduotuve/lt/produktai/pieno-produktai-kiausiniai-ir-suris/c/SH-11",
    "https://www.rimi.lt/e-parduotuve/lt/produktai/duonos-gaminiai-ir-konditerija/c/SH-3",
    "https://www.rimi.lt/e-parduotuve/lt/produktai/mesa-zuvys-ir-kulinarija/c/SH-9",
    "https://www.rimi.lt/e-parduotuve/lt/produktai/bakaleja/c/SH-2"
]

# Funkcija, kuri ištraukia duomenis iš puslapio
def scrape_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    blocks = soup.find_all(class_="product-grid__item")
    data = []

    for block in blocks:
        name = block.find(class_="card__name").get_text().strip()
        href_element = block.find(class_="card__url js-gtm-eec-product-click")
        if href_element:
            href = href_element['href']
            full_href = f"https://www.rimi.lt{href}"  # Pridedame pilną URL
        price_raw = block.find(class_="price-tag card__price")
        if price_raw:
            price_raw = price_raw.get_text().strip()
            price_cleaned = ''.join(filter(str.isdigit, price_raw))
            if len(price_cleaned) > 2:
                price = f"{price_cleaned[:-2]}.{price_cleaned[-2:]}"
            else:
                price = price_cleaned
            data.append([name, price, full_href])
        else:
            data.append([name, "N/A", full_href])

    return data

# Funkcija, kuri apdoroja visus puslapius
def scrape_all_pages(base_url):
    page_num = 1
    all_data = []
    while True:
        url = f"{base_url}?currentPage={page_num}&pageSize=20&query=%3Arelevance%3AallCategories%3A{base_url.split('/')[-1]}%3AassortmentStatus%3AinAssortment"
        data = scrape_page(url)
        if not data:
            break
        all_data.extend(data)
        page_num += 1
    return all_data

# Atidarome CSV failą rašymui
with open("rimi_produktai.csv", 'w', encoding="UTF-8", newline="") as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(['Name', "Price", "Url"])

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(scrape_all_pages, base_url) for base_url in urls]
        for future in concurrent.futures.as_completed(futures):
            data = future.result()
            for row in data:
                csv_writer.writerow(row)

print("Scrapinimas baigtas")