def ini_cheapshark_API(url):
    import requests

    response = requests.get(url)

    if response.status_code == 200:
        dict_deals = response.json()
    else:
        print(response.status_code)

    return dict_deals


def get_dict_stores():

    stores_dict = {}

    stores = ini_cheapshark_API("https://www.cheapshark.com/api/1.0/stores")

    for x in stores:
        stores_dict[x["storeID"]] = x["storeName"]

    return stores_dict


def fill_lists(dict_deals):

    shops_list = []
    names_list = []
    original_price_list = []
    discount_price_list = []
    perc_disc_list = []
    metacritic_list = []

    genre_list = []
    dict_of_stores = get_dict_stores()

    for x in dict_deals:

        names_list.append(x["title"])

        shops_list.append(dict_of_stores[x["storeID"]])        

        original_price_list.append(x["normalPrice"])

        discount_price_list.append(x["salePrice"])
        
        perc_disc_list.append(round( float(x["savings"]), 2) )

        metacritic_list.append(float(x["metacriticScore"]))

        data_title = ini_rawg_API(x["title"])
        genre_list.append(get_genre_list(data_title, x["title"]))

    return  names_list, genre_list, shops_list, original_price_list, discount_price_list, perc_disc_list, metacritic_list
    

def create_cheapshark_df(dict_deals):
    import pandas as pd

    a, b, c, d, e, f, g = fill_lists(dict_deals)

    lista_zip = list(zip(a, b, c, d, e, f, g))

    df = pd.DataFrame(lista_zip, columns=['title', 'genre/s', 'shop', 'og_price', 'dc_price', 'discount_perc', 'metacritic'])

    return df


def save_df(df):
    
    from datetime import datetime

    actual_date = datetime.now().strftime("%d-%m-%Y")
    actual_hour = datetime.now().strftime("%H")

    df.to_csv(f"data/registro_{actual_date}_{actual_hour}horas")


def ini_rawg_API(game):
    
    import os
    from dotenv import load_dotenv
    import requests
    import time

    # Tu clave API de RAWG

    api_key = os.getenv("api_key")

    # URL de la API de RAWG
    base_url = 'https://api.rawg.io/api'

    # Parámetros de la solicitud (ejemplo: buscar juegos con la palabra "cyberpunk")
    params = {
        'key': api_key,
        'search': game,
        'search_exact' : True
    }
    
    time.sleep(1)

    # Hacer la solicitud a la API
    response = requests.get(f'{base_url}/games', params=params)

    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        # Obtener los datos en formato JSON
        data = response.json()

    return data


def get_genre_list(data, game_title):

    genres_list = []

    for x in data["results"]:
        for y in x["genres"]:
            if x["name"] == game_title:
                genres_list.append(y["name"]) 

    return genres_list


# def get_genres_games_list(data):
#     game_title_list = []
#     genres_list = []

#     for x in data["results"]:
        
#         game_title_list.append(x["name"])
#         values = []

#         for y in x["genres"]:
#                 values.append(y["name"])
                
#         genres_list.append(values)
    
#     return game_title_list, genres_list


# def create_rawg_df(data):
#     import pandas as pd
#     a, b = get_genres_games_list(data)

#     mix = list(zip(a, b))
#     df = pd.DataFrame(mix, columns=['title', 'genres'])
#     return df


def main(url):

    dict_deals = ini_cheapshark_API(url)
    df_discounts = create_cheapshark_df(dict_deals)
    save_df(df_discounts)

    return df_discounts