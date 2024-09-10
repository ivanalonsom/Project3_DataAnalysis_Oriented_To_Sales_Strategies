def ini_cheapshark_API(url):
    import requests

    response = requests.get(url)

    if response.status_code == 200:
        dict_resp = response.json()
    else:
        print(response.status_code)

    return dict_resp


def get_dict_stores():

    stores_dict = {}

    stores = ini_API("https://www.cheapshark.com/api/1.0/stores")

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

    dict_of_stores = get_dict_stores()

    for x in dict_deals:

        names_list.append(x["title"])

        shops_list.append(dict_of_stores[x["storeID"]])        

        original_price_list.append(x["normalPrice"])

        discount_price_list.append(x["salePrice"])
        
        perc_disc_list.append(round( float(x["savings"]), 2) )

        metacritic_list.append(float(x["metacriticScore"]))

    return  names_list, shops_list, original_price_list, discount_price_list, perc_disc_list, metacritic_list
    

def create_df(dict_deals):
    import pandas as pd

    a, b, c, d, e, f = fill_lists(dict_deals)

    lista_zip = list(zip(a, b, c, d, e, f))

    df = pd.DataFrame(lista_zip, columns=['title', 'shop', 'og_price', 'dc_price', 'discount_perc', 'metacritic'])

    return df


def save_df(df):
    
    from datetime import datetime

    actual_date = datetime.now().strftime("%d-%m-%Y")

    df.to_csv(f"data/registro_{actual_date}")


def average_disc_vs_shop_bar(df):

    import matplotlib.pyplot as plt

    df_graf_barras = df.groupby('shop')['discount_perc'].mean().reset_index()
    # Same as df_graf_barras = df_all.groupby('shop').agg({'discount_perc' : 'mean'})

    plt.figure(figsize=(15, 9))
    plt.bar(df_graf_barras['shop'], df_graf_barras['discount_perc'])

    # Agregar etiquetas a cada barra
    for i, valor in enumerate(df_graf_barras['discount_perc']):
        plt.text(i, valor + 1, f"{valor:.2f}", ha='center', va='bottom')

    plt.title('Average discount vs Shop')
    plt.xlabel('Shop')
    plt.ylabel('Average discount')
    plt.show()


def min_max_disc_vs_shop_bar(df):
    import numpy as np
    import matplotlib.pyplot as plt

    # Datos de ejemplo (reemplaza esto con tus datos)

    # Calcular los valores máximos y mínimos por tienda
    df_max = df.groupby('shop')['discount_perc'].max().reset_index()
    df_min = df.groupby('shop')['discount_perc'].min().reset_index()

    # Crear un DataFrame combinado
    df_combined = df_max.merge(df_min, on='shop', suffixes=('_max', '_min'))

    # Configuración del gráfico
    fig, ax = plt.subplots(figsize=(18, 10))

    # Crear posiciones para las barras
    bar_width = 0.4
    indices = np.arange(len(df_combined))

    # Graficar las barras
    ax.bar(indices - bar_width/2, df_combined['discount_perc_max'], width=bar_width, label='Max Discount')
    ax.bar(indices + bar_width/2, df_combined['discount_perc_min'], width=bar_width, label='Min Discount')

    # Agregar etiquetas a las barras
    for i, (max_val, min_val) in enumerate(zip(df_combined['discount_perc_max'], df_combined['discount_perc_min'])):
        ax.text(i - bar_width/2, max_val + 1, f"{max_val:.2f}", ha='center', va='bottom')
        ax.text(i + bar_width/2, min_val + 1, f"{min_val:.2f}", ha='center', va='bottom')

    # Configurar etiquetas y título
    ax.set_title('Discount percentage max and min')
    ax.set_xlabel('Shop')
    ax.set_ylabel('Discount %')
    ax.set_xticks(indices)
    ax.set_xticklabels(df_combined['shop'])
    ax.legend()

    plt.show()


def disc_vs_punct_linear(df):
    import matplotlib.pyplot as plt

    df_plat_punt = df[df["metacritic"] > 0][["shop", "discount_perc", "metacritic"]]

    df_plat_punt.sort_values(by="metacritic", ascending=True, inplace=True)

    df_plat_punt

    plt.figure(figsize=(15, 9))
    for tienda in df_plat_punt['shop'].unique():
        df_tienda = df_plat_punt[df_plat_punt['shop'] == tienda]
        plt.plot(df_tienda['metacritic'], df_tienda['discount_perc'], label=tienda, marker='o')

    # Agregamos título y etiquetas a los ejes
    plt.title('Discount vs punctuation')
    plt.xlabel('Punctuation')
    plt.ylabel('Discount')

    # Agregamos leyenda
    plt.legend()

    # Mostramos el gráfico
    plt.show()


def ini_rawg_API():
    




def main(url):

    dict_deals = ini_cheapshark_API(url)
    df_discounts = create_df(dict_deals)
    save_df(df_discounts)

    return df_discounts