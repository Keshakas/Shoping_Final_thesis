from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import csv
import time

# URL sąrašas
urls = [
    "https://lastmile.lt/chain/category/IKI/Pienas-B7UTvIzcguAYSjSplM0z",
    "https://lastmile.lt/chain/category/IKI/Sviestas-margarinas-riebalai-lGecTHdAhyAnZCQCuwhh",
    "https://lastmile.lt/chain/category/IKI/Suris-CdWuu4uUCdxn6AIe4gqc",
    "https://lastmile.lt/chain/category/IKI/Grietine-NQUhVepop3OtR9njG12K",
    "https://lastmile.lt/chain/category/IKI/Varskes-produktai-TVQZUpgOyoRgF6QtXRHA",
    "https://lastmile.lt/chain/category/IKI/Kefyras-rugpienis-pasukos-HLIolFbqYNRWg80KJDQq",
    "https://lastmile.lt/chain/category/IKI/Jogurtai-feVWq0PcvnwNwZnSBycA",
    "https://lastmile.lt/chain/category/IKI/Kiausiniai-JGMOQONuXr63w9SFUIWQ",
    "https://lastmile.lt/chain/category/IKI/Majonezas-r7HtE8CjVMu3zGC8yqby",
    "https://lastmile.lt/chain/category/IKI/Vaisiai-iSYTdWjFGh5YWglqphtj",
    "https://lastmile.lt/chain/category/IKI/Darzoves-R9SDZX71J0Qapuvm1Lgp",
    "https://lastmile.lt/chain/category/IKI/Uogos-TyLpkJrj4VvzdZTgry59",
    "https://lastmile.lt/chain/category/IKI/Grybai-VX72LbxC8cV0A1Kh40k6",
    "https://lastmile.lt/chain/category/IKI/Kepti-duonos-gaminiai-DLoQF9DWugzS6QDi9Iqn",
    "https://lastmile.lt/chain/category/IKI/Duona-FtgjCgmmcpD8W7bFn94C",
    "https://lastmile.lt/chain/category/IKI/Batonas-CXmRw5Eqxzb8RvbLiRZE",
    "https://lastmile.lt/chain/category/IKI/Duonos-pakaitalai-GzdonUwqd5iAXyISiSNu",
    "https://lastmile.lt/chain/category/IKI/Duonos-pyragai-keksai-ir-keksiukai-ex8Rhx6CSf091zVMlfdB",
    "https://lastmile.lt/chain/category/IKI/Dziuvesiai-meduoliai-riestainiai-ir-javinukai-mHAVj1rAYbfzEpDMk4nI",
    "https://lastmile.lt/chain/category/IKI/Bandeles-spurgos-kibinai-guVfF3XHMnBGq0LyD2oA",
    "https://lastmile.lt/chain/category/IKI/Konditerija-lyjTy293mSE1V6NPmWgs",
    "https://lastmile.lt/chain/category/IKI/Sviezia-mesa-1CKDIcxEpY7b2UHbAsaw",
    "https://lastmile.lt/chain/category/IKI/Sviezia-paukstiena-V6LgkRAG0FtJxk92EedA",
    "https://lastmile.lt/chain/category/IKI/Mesos-ir-paukstienos-gaminiai-bwjLXqWL9aE79yQ8gXl9",
    "https://lastmile.lt/chain/category/IKI/Marinuota-mesa-ir-paukstiena-YNBc38VZOEZvY2gMcZhr",
    "https://lastmile.lt/chain/category/IKI/Sviezia-zuvis-ir-juru-gerybes-aAztRXgfDPJvZMHJ4N8m",
    "https://lastmile.lt/chain/category/IKI/Zuvies-gaminiai-uxZ0bIW63yS6X9E2Wrwt",
    "https://lastmile.lt/chain/category/IKI/Kulinarija-z54qJvi1a0tFeOpMI4N1",
    "https://lastmile.lt/chain/category/IKI/Aliejus-ir-actas-alSGOxSJTCEUc4AYVimh",
    "https://lastmile.lt/chain/category/IKI/Cukrus-saldikliai-medus-DVlT42gJS3sevRSkHkWE",
    "https://lastmile.lt/chain/category/IKI/Kava-kakava-kavos-gerimai-eFlHBDHmobDg7BPxTBYa",
    "https://lastmile.lt/chain/category/IKI/Arbata-fi49LFhlfK8LVZN73CBd",
    "https://lastmile.lt/chain/category/IKI/Makaronai-hww6HY7FA1of6l2tJSsO",
    "https://lastmile.lt/chain/category/IKI/Miltai-Qcr3pLFVc8H5Jznf4l1f",
    "https://lastmile.lt/chain/category/IKI/Kruopos-RkxJvEZNHwXHsT4H9U3O",
    "https://lastmile.lt/chain/category/IKI/Ryziai-wqH0UDucPSMqw11XaYe0",
    "https://lastmile.lt/chain/category/IKI/Ankstines-darzoves-ISAig48P42h8ZXDBaPeZ",
    "https://lastmile.lt/chain/category/IKI/Padazai-ir-uztepeles-QAurOjd8UT5526MFHpIn",
    "https://lastmile.lt/chain/category/IKI/Marinuotas-konservuotas-maistas-fj9o35CmfqVMtXOIMlRV",
    "https://lastmile.lt/chain/category/IKI/Sausi-pusryciai-dribsniai-ir-javainiu-batoneliai-ugS5OMkfCm7fLWWe8j8U",
    "https://lastmile.lt/chain/category/IKI/Riesutai-seklos-dziovinti-vaisiai-uogos-FKEA5rBnkQe9QXzOhUh4",
    "https://lastmile.lt/chain/category/IKI/Greitai-paruosiamas-maistas-tzQHf1Pq60Y2m3V7dyCb",
    "https://lastmile.lt/chain/category/IKI/Specialus-maistas-XCmQGbiqAryyKyYKuPbr",
    "https://lastmile.lt/chain/category/IKI/Maisto-ruosimo-priedai-KoJJP7J8EvEJpoNxv8qj",
    "https://lastmile.lt/chain/category/IKI/Pasaulio-virtuves-Hd0GxIHLNoFnmPntrBR1",
    "https://lastmile.lt/chain/category/IKI/Prieskoniai-xcDHOtxyRKocg4hsMzkf",
]

# Atidarome CSV failą rašymui
with open("iki_produktai.csv", 'w', encoding="UTF-8", newline="") as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(['Name', "Price"])

    # Nustatome Chrome headless režimą
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Veikia be grafinio lango
    chrome_options.add_argument("--no-sandbox")  # Linux sistemos suderinamumas
    chrome_options.add_argument("--disable-dev-shm-usage")  # Pagerina veikimą

    # Paleidžiame Chrome su nurodytais nustatymais
    driver = webdriver.Chrome(options=chrome_options)

    for url in urls:
        driver.get(url)

        # Laukiame, kol puslapis užsikraus
        time.sleep(1)  # Užlaikymas 1 sekundę prieš pereinant prie BeautifulSoup

        # Naudojame BeautifulSoup duomenų nuskaitymui
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Randame produktų blokus
        blocks = soup.find_all(
            class_="_dsp-flex _ai-stretch _fd-row _fb-auto _bxs-border-box _pos-relative _mih-0px _miw-0px _fs-1 _fg-1 _w-10037")

        for block in blocks:
            try:
                name = block.find(
                    class_="_dsp-flex _ai-stretch _fd-column _fb-auto _bxs-border-box _pos-relative _mih-0px _miw-0px _fs-0 _pt-1316332222 _pb-1316332222").get_text().strip()
                price = block.find(
                    class_="_dsp-flex _fd-row _fb-auto _bxs-border-box _pos-relative _mih-0px _miw-0px _fs-0 _ai-center").get_text().strip()
                price = price.split("€ ")[1]  # Paimame tik kainą po '€'

                # Įrašome pavadinimą ir kainą į CSV
                csv_writer.writerow([name, price])
                print(name)
                print(price)
                print("----------------------------------")
            except AttributeError:
                # Jei koks elementas nerandamas, praleidžiame jį
                continue

    # Uždarome naršyklę
    driver.quit()
