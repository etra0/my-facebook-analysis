# Analisis de mi Facebook

* [Introducción](https://github.com/etrastyle/my-facebook-analysis#introducción)
* [Resultados](https://github.com/etrastyle/my-facebook-analysis#resultados)
* [Requisitos](https://github.com/etrastyle/my-facebook-analysis#requisitos)
* [Instrucciones](https://github.com/etrastyle/my-facebook-analysis#instrucciones)

# Introducción 

Análisis de datos de mis estados de Facebook hecho totalmente en `python3`.

Actualmente puede generar 4 gráficos:
* La cantidad de likes por año
* La cantidad de <3 al año
* La cantidad de improperios
* top 20 amigos que dan más likes.

## Resultados

![likes](https://github.com/etrastyle/my-facebook-analysis/blob/master/out/most_liked_year.png)
![loved](https://github.com/etrastyle/my-facebook-analysis/blob/master/out/most_loved_year.png)
![swear](https://github.com/etrastyle/my-facebook-analysis/blob/master/out/my_favourite_swear.png)

## Requisitos

* Python 3
* [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/)
* [pandas](https://pandas.pydata.org/pandas-docs/stable/index.html)
* [matplotlib](https://matplotlib.org/)
* [requests](http://docs.python-requests.org/en/master/)

## Instrucciones

1. Descargar el
[facebook-sdk](https://facebook-sdk.readthedocs.io/en/latest/install.html)
para python3.

2. Activar el virtualenv según las instrucciones
del sdk de facebook

3. Ejecutar `python3 get_data.py`

4. Salir del virtualenv escribiendo `deactivate`

5. Ejecutar `python3 plot.py`
