def ini_API(url):
    import requests
    # Parámetros para la solicitud (puedes personalizarlos según la documentación de la API)
    # params = {
    #     "storeID": 25,     # ID de la tienda (opcional)
    #     "upperPrice": 100, # Precio máximo (opcional)
    #     "pageNumber": 0   # Número de página (opcional)
    # }

    # Realizar la solicitud GET
    response = requests.get(url)

    if response.status_code == 200:
        dict_resp = response.json()
    else:
        print(response.status_code)

    return dict_resp


def dict_stores():

    dict_tiendas = {}

    stores = ini_API("https://www.cheapshark.com/api/1.0/stores")

    for x in stores:
        dict_tiendas[x["storeID"]] = x["storeName"]

    return dict_tiendas


def fill_lists(dict_deals):

    shops_list = []
    names_list = []
    original_price_list = []
    discount_price_list = []
    perc_disc_list = []
    metacritic_list = []

    dict_of_stores = dict_stores()

    for x in dict_deals:
        shops_list.append(dict_of_stores[x["storeID"]])
        
        names_list.append(x["title"])

        original_price_list.append(x["normalPrice"])

        discount_price_list.append(x["salePrice"])
        
        perc_disc_list.append(round( float(x["savings"]), 2) )

        metacritic_list.append(float(x["metacriticScore"]))

    return shops_list, names_list, original_price_list, discount_price_list, perc_disc_list, metacritic_list
    

def create_df(dict_deals):

    a, b, c, d, e, f = fill_lists(dict_deals)

    
