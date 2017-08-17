# Analisis de mi Facebook

Análisis de datos de mis estados de Facebook hecho totalmente en `python3`.

## Resultados

![swear](https://github.com/etrastyle/my-facebook-analysis/blob/master/out/my_favourite_swear.png)
![likes](https://github.com/etrastyle/my-facebook-analysis/blob/master/out/most_liked_year.png)
![loved](https://github.com/etrastyle/my-facebook-analysis/blob/master/out/most_loved_year.png)

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
