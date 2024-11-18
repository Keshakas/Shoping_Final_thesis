import pandas as pd

def get_filtered_lowest_price(file_path, product_name, fat_content, quantity):
    # Patikriname, ar visi parametrai yra pateikti
    if not all([product_name, fat_content, quantity]):
        return None  # Jei trūksta bent vieno parametro, grąžiname None

    # Nuskaityti CSV failą į DataFrame
    with open(file_path, 'r', encoding='utf-8') as file:
        df = pd.read_csv(file)

    # Filtruoti pagal kriterijus
    filtered_df = df[
        df['Name'].str.contains(product_name, case=False, na=False) &
        df['Name'].str.contains(fat_content, case=False, na=False) &
        df['Name'].str.contains(quantity, case=False, na=False)
    ]

    # Patikriname, ar yra filtruotų eilučių
    if not filtered_df.empty:
        # Randame eilutę su mažiausia kaina
        lowest_price_row = filtered_df.loc[filtered_df['Price'].idxmin()]
        return {
            'price': lowest_price_row['Price'],
            'name': lowest_price_row['Name']
        }

    return None


def get_lowest_price_from_csv(file_path, product_name):
    # Nuskaitome CSV failą į DataFrame
    with open(file_path, 'r', encoding='utf-8') as file:
        df = pd.read_csv(file)

    # Filtruojame pagal produkto pavadinimą (naudojame case-insensitive paiešką)
    filtered_df = df[df['Name'].str.contains(product_name, case=False, na=False)]

    if filtered_df.empty:
        return None, None  # Jei nėra rezultatų, grąžiname tuščią reikšmę

    # Randame eilutę su mažiausia kaina
    min_price_row = filtered_df.loc[filtered_df['Price'].idxmin()]

    # Grąžiname pilną pavadinimą ir mažiausią kainą
    return min_price_row['Name'], min_price_row['Price']