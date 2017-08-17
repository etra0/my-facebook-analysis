import time as t
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams['font.sans-serif'] = 'Open Sans'
plt.style.use("fivethirtyeight")

def title(ax, fig, title, subtitle='', credits='', rect=[0, 0, 1, 0.93]):
    ax.text(0.0, 1.04, title, fontsize=20, va='bottom', fontweight="bold", transform=ax.transAxes)
    ax.text(0.0, 1.0, subtitle, fontsize=14, alpha=0.5, transform=ax.transAxes)
    ax.text(1., -0.13, credits, fontsize=10, alpha=0.3, va='bottom', ha='right', transform=ax.transAxes)
    fig.tight_layout(rect=rect)

def prepare_data(filename):
    df = pd.read_csv(filename, sep=";")
    
    # first thing: parse time
    df['date'] = df['date'].apply(lambda x: t.strptime(x, "%Y-%m-%dT%H:%M:%S+0000"))

    return df

def generate_fan_csv(df):
    """
    Esta función genera el csv con los amigos y la cantidad de likes
    que han dado cada uno de ellos a tus estados.
    """
    friends = dict()
    df['list_likes'] = df['list_likes'].apply(lambda x: eval(x))

    for i, row in df.iterrows():
        for friend in row['list_likes']:
            if friend not in friends:
                friends[friend] = 0
            friends[friend] += 1

    with open("friends.csv", "w") as f:
        f.write("friend;q\n")
        for friend in friends:
            f.write("%s;%d\n" % (friend, friends[friend]))

def most_liked_year(df):
    """
    Genera un gráfico donde cuenta la cantidad de likes que tuviste al año.
    """
    grouped = df.groupby(by=df['date'].map(lambda x: x.tm_year)).sum()
    grouped = grouped.loc[grouped['q_likes'] > 0]

    const = 2.3
    fig = plt.figure(figsize=(4*const, 3*const))
    ax = fig.add_subplot(1, 1, 1)

    ax.bar(grouped.index, grouped['q_likes'], color='#00b5dd')

    ax.set_xlabel("Año")
    ax.set_ylabel("Cantidad")
    title(ax, fig, "Cantidad de likes al año", "En mis estados de Facebook", "Por Sebastián Aedo, http://saedo.me")
    fig.savefig("out/most_liked_year.png", dpi=300)

def most_loved_year(df):
    """
    Genera un gráfico donde cuenta la cantidad de <3 que has colocado
    en los estados por año.
    """
    loved_df = df
    loved_df['contains_heart'] = loved_df['message'].map(lambda x: '<3' in x)
    loved_df = loved_df.loc[loved_df['contains_heart']]

    grouped = df.groupby(by=loved_df['date'].map(lambda x: x.tm_year)).count()

    const = 2.3
    fig = plt.figure(figsize=(4*const, 3*const))
    ax = fig.add_subplot(1, 1, 1)

    ax.bar(grouped.index, grouped['message'], color='#fd8550')
    ax.set_xlabel("Año")
    ax.set_ylabel("Cantidad")
    title(ax, fig, "Frecuencia de uso de <3", "En mis estados de Facebook", "Por Sebastián Aedo, http://saedo.me")
    fig.savefig("out/most_loved_year.png", dpi=300)

def friend_most_likes():
    """
    Genera un gráfico con las 20 personas que más le han dado likes
    a tus estados
    """
    df = pd.read_csv('friends.csv', sep=";")
    df = df.sort_values(by='q', ascending = False)

    const = 2.3
    fig = plt.figure(figsize=(4*const, 3*const))
    ax = fig.add_subplot(1, 1, 1)

    df.iloc[:20].plot.barh('friend', 'q', color="#00b5dd", ax=ax, legend=False, width=0.8)
    fig.gca().invert_yaxis()
    title(ax, fig, "Cantidad de likes según amigos",
            "En mis estados de Facebook",
            "Por Sebastián Aedo, http://saedo.me",
            [0, 0.045, 1, 0.93])
    ax.set_xlabel("Cantidad")
    ax.set_ylabel("")
    fig.savefig("out/friend_most_likes.png", dpi=300)

def clean_word(text):
    """
    sirve para limpiar los strings con caracteres no deseados.
    """
    chars = '"\'!?¿¡;,._:'
    for char in chars:
        text = text.replace(char, '')

    text = text.replace("\n", " ").split(" ")
    return text

def my_favourite_swear(df):
    """
    Genera un gráfico con la cantidad de improperios totales que has hecho
    en los estados de Facebook.
    """
    bad_words = {
        "weón": [["wn", "weón", "weon", "hueón", "hueon", 'weones', 'hueones'], 0],
        "ctm": [["conchesumadre", "conchetumare", "csm", "ctm", 'conchesumadres', 'conshetumare'], 0],
        "cagar": [["cagá", "cagar", "cagué", "caga", "cague", "cagan"], 0],
        "chucha": [["chucha", "chuchá", "chuchada", "xuxa"], 0],
        "ql": [["ql", "culiao", "culeado", "culiado", "cl", "kl", "culiaos, qls"], 0],
        "mierda": [['mierda'], 0],
        "wea": [['wea', 'weá', "weás", "hueás", "hueas"], 0],
        "puta": [["puta"], 0]
        }

    contains_bad_word = 0
    max_container = 0
    for index, row in df.iterrows():
        # pueden haber mensajes con más de una línea
        message = row['message']
        message = clean_word(message)
        contains = False
        temp_container = 0
        for word in message:
            word = word.lower()
            for bw in bad_words:
                for bw_version in bad_words[bw][0]:
                    if bw_version == word:
                        bad_words[bw][1] += 1

                        # this count if there is at least one bad word
                        contains = True

                        # count the bad words per state
                        temp_container += 1
        if temp_container > max_container:
            max_container = temp_container
            print(row['message'])

        contains_bad_word += contains

    data = [(bw, bad_words[bw][1]) for bw in bad_words]
    data = sorted(data, key = lambda x: x[1], reverse=True)

    const = 2.3
    fig = plt.figure(figsize=(4*const, 3.5*const))
    ax = fig.add_subplot(1, 1, 1)

    ind = np.arange(len(data))
    width = 0.8

    # colormap thing
    colormap = plt.get_cmap('gist_heat')
    y_data = list(map(lambda x: x[1], data))
    colors = [colormap(i) for i in np.linspace(0.6, 0, max(y_data))]
    f_colors = [colors[y-1] for y in y_data]

    ax.bar(ind + width / 2, list(map(lambda x: x[1], data)),
            color=f_colors, width=width)
    ax.set_xticks(ind + width/2)
    ax.set_xticklabels(list(map(lambda x: x[0], data)))

    title(ax, fig, "Mi chuchá favorita <3",
            "Según mis estados de Facebook",
            "",
            [0.05, 0.2, 1, 0.93])
    ax.set_xlabel("")
    ax.set_ylabel("Cantidad")

    data_to_print = {
            'freq': int((contains_bad_word/len(df))*100),
            'cant': max_container,
            'total': len(df)
            }
    text = """
{freq} de cada 100 estados contienen al menos un garabato.
El estado con más chuchás contiene {cant} garabatos.
Estados analizados: {total}
    """.strip().format(**data_to_print)
    ax.text(0.00, -0.1, text, ha='left', fontsize=20, transform=ax.transAxes, va='top')

    fig.savefig("out/my_favourite_swear.png", dpi=300)

if __name__ == '__main__':
    df = prepare_data('../data.csv')
    generate_fan_csv(df)
#    friend_most_likes()
#    most_loved_year(df)
#    most_liked_year(df)
    my_favourite_swear(df)
