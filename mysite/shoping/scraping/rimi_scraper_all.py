from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import csv
import time

# URL sąrašas
urls = [
    "https://www.rimi.lt/e-parduotuve/lt/produktai/vaisiai-darzoves-ir-geles/c/SH-15",
    "https://www.rimi.lt/e-parduotuve/lt/produktai/pieno-produktai-kiausiniai-ir-suris/c/SH-11",
    "https://www.rimi.lt/e-parduotuve/lt/produktai/duonos-gaminiai-ir-konditerija/c/SH-3",
    "https://www.rimi.lt/e-parduotuve/lt/produktai/mesa-zuvys-ir-kulinarija/c/SH-9",
    "https://www.rimi.lt/e-parduotuve/lt/produktai/bakaleja/c/SH-2"
]

# Atidarome CSV failą rašymui
with open("rimi_produktai.csv", 'w', encoding="UTF-8", newline="") as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(['Name', "Price"])

    # Nustatome Chrome headless režimą
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Veikia be grafinio lango
    chrome_options.add_argument("--no-sandbox")  # Linux sistemos suderinamumas
    chrome_options.add_argument("--disable-dev-shm-usage")  # Pagerina veikimą

    # Paleidžiame Chrome su nurodytais nustatymais
    driver = webdriver.Chrome(options=chrome_options)

    for base_url in urls:
        page_num = 1
        while True:
            # Generuojame URL su puslapio numeriu
            url = f"{base_url}?currentPage={page_num}&pageSize=20&query=%3Arelevance%3AallCategories%3A{base_url.split('/')[-1]}%3AassortmentStatus%3AinAssortment"
            driver.get(url)

            # Naudojame BeautifulSoup duomenų nuskaitymui
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Randame produktų blokus
            blocks = soup.find_all(class_="product-grid__item")

            # Jeigu nėra daugiau blokų, nutraukiame ciklą
            if not blocks:
                print(f"No more pages for {base_url}")
                break

            # Surandame ir įrašome pavadinimą bei kainą
            for block in blocks:
                name = block.find(class_="card__name").get_text().strip()
                price_raw = block.find(class_="price-tag card__price")
                if price_raw:
                    price_raw = price_raw.get_text().strip()
                    price_cleaned = ''.join(filter(str.isdigit, price_raw))
                    if len(price_cleaned) > 2:
                        price = f"{price_cleaned[:-2]}.{price_cleaned[-2:]}"
                    else:
                        price = price_cleaned
                    csv_writer.writerow([name, price])
                    print(name)
                    print(price)
                    print("----------------------------------")
                else:
                    # Jei nėra kainos, galima įrašyti tuščią kainą arba praleisti įrašą
                    csv_writer.writerow([name, "N/A"])
                    print(name)
                    print("N/A")
                    print("----------------------------------")

            page_num += 1
            time.sleep(0.01)  # Pridėkime nedidelį laukimo laiką, kad būtų išvengta serverio užblokavimo

    driver.quit()
