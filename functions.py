def ini_cheapshark_API(url):

    """
    This function connects to the CheapShark API using the provided URL to retrieve a list of game deals.
    
    Parameters:
        url (str): The web address (URL) that leads to the CheapShark API.
    
    Returns:
        dict: A dictionary of game deals if the connection is successful, otherwise prints an error code.
    
    Purpose:
        This function sends a request to the CheapShark API, which stores information about discounted video games.
        If the connection is successful, it returns the data in a dictionary format, which can then be used for further analysis.
        If not, it prints an error code so we know what went wrong.
    """
        
    import requests

    # params = {
    #     'sortBy' : 'Recent'
    # }

    response = requests.get(url)
    # response = requests.get(url, params=params)   We could use this line instead of the previous one if we wanted to sort by the most recently added games.

    if response.status_code == 200:
        dict_deals = response.json()
    else:
        print(response.status_code)

    return dict_deals


def ini_rawg_API(game):

    """
    This function connects to the RAWG API to search for information about a specific video game.
    
    Parameters:
        game (str): The title of the video game being searched for.
    
    Returns:
        dict: A dictionary containing information about the video game from the RAWG API.
    
    Purpose:
        To retrieve detailed information about a video game from the RAWG API, including its genre and release date.
    """
    
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
    
    time.sleep(0.5)

    # Hacer la solicitud a la API
    response = requests.get(f'{base_url}/games', params=params)

    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        # Obtener los datos en formato JSON
        data = response.json()

    return data


def get_dict_stores():

    """
    This function creates a dictionary that maps store IDs to store names.
    
    Returns:
        dict: A dictionary where the keys are store IDs and the values are store names.
    
    Purpose:
        To retrieve a list of stores from the CheapShark API and convert it into a dictionary, making it easier to access the name of each store based on its ID.
    """

    stores_dict = {}

    stores = ini_cheapshark_API("https://www.cheapshark.com/api/1.0/stores")

    for x in stores:
        stores_dict[x["storeID"]] = x["storeName"]

    return stores_dict


def fill_lists(dict_deals):

    """
    This function processes the data from CheapShark API to create multiple lists about video games, including titles, stores, prices, discounts, and more.
    
    Parameters:
        dict_deals (dict): A dictionary containing information about discounted video games.
    
    Returns:
        tuple: A collection of lists that store various details about the games, such as their names, genres, release dates, and pricing.
    
    Purpose:
        To break down the data from the CheapShark API into separate lists that store specific information, making it easier to analyze and create dataframes.
    """

    shops_list = []
    dict_of_stores = get_dict_stores()
    names_list = []
    original_price_list = []
    discount_price_list = []
    perc_disc_list = []
    metacritic_list = []

    
    genre_list = []
    released_list = []
    

    for x in dict_deals:

        names_list.append(x["title"])

        shops_list.append(dict_of_stores[x["storeID"]])        

        original_price_list.append(x["normalPrice"])

        discount_price_list.append(x["salePrice"])
        
        perc_disc_list.append(round( float(x["savings"]), 2) )

        metacritic_list.append(float(x["metacriticScore"]))

        data_title = ini_rawg_API(x["title"])
        genre_list.append(get_genre_list(data_title, x["title"]))
        released_list.append(get_release_date_list(data_title) )

        #released_list.append(x["releaseDate"])


    return  names_list, genre_list, released_list ,shops_list, original_price_list, discount_price_list, perc_disc_list, metacritic_list
    

def create_cheapshark_df(dict_deals):

    """
    This function organizes game data into a table (DataFrame) using the lists created from the API data.
    
    Parameters:
        dict_deals (dict): A dictionary of video game deals from the CheapShark API.
    
    Returns:
        DataFrame: A pandas DataFrame containing details about video game deals, including the title, genre, release date, prices, and more.
    
    Purpose:
        To transform the data from the CheapShark API into a structured table format (DataFrame) that is easier to work with for analysis.
    """
    import pandas as pd

    a, b, c, d, e, f, g, h = fill_lists(dict_deals)

    lista_zip = list(zip(a, b, c, d, e, f, g, h))

    df = pd.DataFrame(lista_zip, columns=['title', 'genre', 'release_date', 'shop', 'og_price', 'dc_price', 'discount_perc', 'metacritic'])

    return df


def save_df(df):

    """
    This function saves the DataFrame of video game deals as a CSV file with the current date and time in its name.
    
    Parameters:
        df (DataFrame): The DataFrame containing the video game deal data.
    
    Purpose:
        To save the table of game data to a CSV file, making it easy to access and share later.
    """
    
    from datetime import datetime

    actual_date = datetime.now().strftime("%d-%m-%Y")
    actual_hour = datetime.now().strftime("%H")

    df.to_csv(f"data/registro_{actual_date}_{actual_hour}horas")


def get_genre_list(data, game_title):

    """
    This function extracts the genres of a specific video game from the RAWG API data.
    
    Parameters:
        data (dict): The data retrieved from the RAWG API.
        game_title (str): The title of the video game being analyzed.
    
    Returns:
        list: A list of genres associated with the video game.
    
    Purpose:
        To collect the genres of the game by searching the RAWG API results and filtering based on the game's title.
    """

    genres_list = []

    for x in data["results"]:
        for y in x["genres"]:
            if x["name"] == game_title:
                genres_list.append(y["name"]) 

    return genres_list


def get_release_date_list(data):

    """
    This function retrieves the release date of a video game from the RAWG API data.
    
    Parameters:
        data (dict): The data retrieved from the RAWG API.
    
    Returns:
        str: The release date of the video game, or None if no release date is found.
    
    Purpose:
        To extract the release date of the game from the RAWG API results.
    """

    if "results" in data and len(data["results"]) > 0:
            result = data["results"][0]
            if "released" in result:
                return result["released"]
    return None


def unroll_list_from_dfcolumn(df, column):

    """
    This function expands a list within a DataFrame column into separate rows.
    
    Parameters:
        df (DataFrame): The DataFrame containing the column with lists.
        column (str): The name of the column to expand.
    
    Returns:
        DataFrame: The updated DataFrame with lists unrolled into individual rows.
    
    Purpose:
        To break down a column containing lists into multiple rows, making the DataFrame easier to analyze.
    """

    df = df.explode(column)
    df.dropna(subset=column, inplace=True)
    return df


def clean_df_releases(df):

    """
    This function cleans the DataFrame by removing rows with missing release dates and sorting it by release date.
    
    Parameters:
        df (DataFrame): The DataFrame containing the game data.
    
    Returns:
        DataFrame: The cleaned and sorted DataFrame.
    
    Purpose:
        To remove entries without a release date and to sort the remaining games by their release dates.
    """

    df.dropna(subset="release_date").reset_index(drop=True).sort_values("release_date")
    return df


def main(url):

    """
    This is the main function that combines all other functions to retrieve, process, and save video game deal data from the CheapShark API.
    
    Parameters:
        url (str): The web address (URL) of the CheapShark API that provides the video game deals.
    
    Returns:
        DataFrame: A pandas DataFrame containing the final data on video game deals.
    
    Purpose:
        To run the complete process: downloading data, processing it, organizing it into a table, and saving it for later use.
    """
    
    dict_deals = ini_cheapshark_API(url)
    df_discounts = create_cheapshark_df(dict_deals)
    save_df(df_discounts)

    return df_discounts