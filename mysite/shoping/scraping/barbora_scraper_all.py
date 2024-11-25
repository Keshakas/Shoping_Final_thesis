from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import csv

# Nuorodų sąrašas
urls = [
    "https://www.barbora.lt/pieno-gaminiai-ir-kiausiniai",
    "https://www.barbora.lt/darzoves-ir-vaisiai",
    "https://www.barbora.lt/duonos-gaminiai-ir-konditerija",
    "https://www.barbora.lt/mesa-zuvis-ir-kulinarija",
    "https://www.barbora.lt/bakaleja"
]

# Atidarome CSV failą rašymui
with open("barbora_produktai.csv", 'w', encoding="UTF-8", newline="") as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(['Category', 'Name', "Price"])  # Pridedame antraštę

    # Nustatome Chrome headless režimą
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Įjungia veikimą be atidaryto lango
    chrome_options.add_argument("--no-sandbox")  # Papildomas nustatymas Linux sistemoms
    chrome_options.add_argument("--disable-dev-shm-usage")  # Pagerina veikimą

    # Paleidžiame Chrome su nurodytais nustatymais
    driver = webdriver.Chrome(options=chrome_options)

    for url in urls:
        category = url.split("/")[-1]  # Paimame paskutinį URL segmentą kaip kategorijos pavadinimą
        page_num = 1

        while True:
            # Sukuriame dinaminį URL su puslapio numeriu
            full_url = f"{url}?page={page_num}"
            driver.get(full_url)

            # Naudojame BeautifulSoup duomenų nuskaitymui
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Randame prekių blokus
            blocks = soup.find_all(class_="tw-flex-shrink-0 tw-list-none tw-w-full")

            # Jeigu nėra daugiau blokų, nutraukiame ciklą
            if not blocks:
                break

            # Surandame ir išsaugome pavadinimą bei kainą
            for block in blocks:
                name = block.find(class_="tw-block").get_text().strip()
                price = block.find(class_="tw-pb-1").get_text().strip()
                price = price.split("€")[0]  # Paimame tik pirmąją dalį prieš '€'
                csv_writer.writerow([category, name, price])  # Rašome į CSV failą
                print(f"Kategorija: {category}, Pavadinimas: {name}, Kaina: {price}")

            page_num += 1

    driver.quit()
