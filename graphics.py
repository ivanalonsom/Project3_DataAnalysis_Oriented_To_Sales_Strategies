def average_disc_vs_shop_bar(df):

    import matplotlib.pyplot as plt

    df_graf_barras = df.groupby('shop')['discount_perc'].mean().reset_index()
    # Same as df_graf_barras = df_all.groupby('shop').agg({'discount_perc' : 'mean'})

    plt.figure(figsize=(18, 12))
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


def linear_graph_discounts_vs_punct_linear(df):
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


def genre_vs_mean_discount_bar(df):
    import matplotlib.pyplot as plt

    df_graf_barras = df.groupby('genre')['discount_perc'].mean().reset_index()

    plt.figure(figsize=(16, 10))
    plt.bar(df_graf_barras['genre'], df_graf_barras['discount_perc'])

    # Agregar etiquetas a cada barra
    for i, valor in enumerate(df_graf_barras['discount_perc']):
        plt.text(i, valor + 1, f"{valor:.2f}", ha='center', va='bottom')

    plt.title('Average discount vs genre')
    plt.xlabel('Genre')
    plt.ylabel('Average discount')
    plt.show()


def circular_pie_chart_genres(df):
    import matplotlib.pyplot as plt

        # Crea un gráfico circular con el conteo de veces que aparece cada valor en la columna "genre"
    values = df['genre'].value_counts().values
    labels = df['genre'].value_counts().index

    plt.pie(values, labels=labels, autopct='%1.1f%%', textprops={'fontsize': 8, 'fontweight': 'normal'})

        # Agrega un título al gráfico
    plt.title('Genres count')

        # Muestra el gráfico
    plt.show()
        

def linear_graph_discounts_vs_releasedate(df):
    import matplotlib.pyplot as plt
    import pandas as pd

    df_plat_punt = df[df["metacritic"] > 0][["shop", "discount_perc", "release_date", "metacritic"]]

    # Convertir la columna "release_date" a datetime
    df_plat_punt['release_date'] = pd.to_datetime(df_plat_punt['release_date'])

    # Extraer el mes y año de lanzamiento
    df_plat_punt['month_year'] = df_plat_punt['release_date'].dt.to_period('M').dt.to_timestamp()

    # Ordenar por "month_year"
    df_plat_punt.sort_values(by="month_year", ascending=True, inplace=True)

    plt.figure(figsize=(16, 10))
    for tienda in df_plat_punt['shop'].unique():
        df_tienda = df_plat_punt[df_plat_punt['shop'] == tienda]
        plt.plot(df_tienda['month_year'], df_tienda['discount_perc'], label=tienda, marker=None)

    # Agregamos título y etiquetas a los ejes
    plt.title('Discount vs Release Date')
    plt.xlabel('Release Date')
    plt.ylabel('Discount')

    # Agregamos leyenda
    plt.legend()

    # Rotar las etiquetas del eje X para mejor lectura
    plt.xticks(rotation=45)

    # Mostramos el gráfico
    plt.show()
