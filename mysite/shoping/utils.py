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
    try:
        # Nuskaitome CSV failą
        with open(file_path, 'r', encoding='utf-8') as file:
            df = pd.read_csv(file)
        print(f"Loaded CSV:\n{df.head()}")

        # Patikriname, ar stulpeliai egzistuoja
        if 'Name' not in df.columns or 'Price' not in df.columns:
            print("Error: 'Name' or 'Price' columns missing in CSV")
            return None

        # Konvertuojame 'Price' į skaitmeninį formatą
        df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

        # Lankstus filtravimas pagal `product_name`
        search_terms = product_name.lower().split()
        print(f"Search terms: {search_terms}")

        filtered_df = df[df['Name'].str.lower().apply(
            lambda x: all(term in x for term in search_terms)
        )]
        print(f"Filtered DataFrame:\n{filtered_df}")

        # Jei filtravimas grąžina reikšmes
        if not filtered_df.empty:
            # Surandame minimalią kainą
            min_row = filtered_df.loc[filtered_df['Price'].idxmin()]
            print(f"Lowest price row: {min_row}")
            return {
                'price': float(min_row['Price']),  # Tik skaičius
                'name': min_row['Name']  # Pilnas pavadinimas
            }
        else:
            print("No matching products found in CSV")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None