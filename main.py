from datetime import datetime
from datetime import timedelta
from Visualización import *
from Actualización import *
from Errores import error_handling

import pandas as pd
import yfinance as yf
import sqlite3
import json
import plotly.express as px

ticker_name = plot_ticker
save_ticker = save_ticker_data
save_metadata = save_ticker_metadata
check_ticker = check_ticker_data
get_ticker = get_ticker_data
error = error_handling

exit_command = False

while not exit_command:
    user_command = input("Por favor elija entre: 'get', 'check' y 'display'\n").lower()

    if user_command == 'get':
        ticker = input("Ingrese el ticker: ").upper()
        st_date = input("Ingrese la fecha de inicio (YYYY-MM-DD): ")
        fn_date = input("Ingrese la fecha de finalización (YYYY-MM-DD): ")

        get_error_code = get_ticker_data(ticker, st_date, fn_date)
        if get_error_code == 1:
            print("El Ticker es invalido, favor de verificar e intentar nuevamente.")
        elif get_error_code == 2:
            print("El Ticker es invalido, favor de verificar e intentar nuevamente.")
        elif get_error_code == 3:
            print("El rango elegido ha excedido las capacidades de este sistema, por favor ingrese un rango más corto.")

    elif user_command == 'check':
        ticker = input("Ingrese el ticker: ").upper()
        ticker_meta_data = check_ticker_data(ticker)

        if ticker_meta_data is None:
            print("No existe información de este ticker.")
        else:
            print("Fecha de Inicio: " + ticker_meta_data["start_date"])
            print("Fecha de Finalización: " + ticker_meta_data["end_date"])

    elif user_command == 'display':
        ticker = input("Ingrese el ticker: ").upper()
        ticker_meta_data = check_ticker_data(ticker)

        if ticker_meta_data is None:
            print("No existe información de este ticker.")
        else:
            plot_ticker(ticker)

    elif user_command == 'exit':
        exit_command = True

    else:
        print("Comando Invalido.")

print("Gracias por utilizar nuestros servicios, que tenga un gran día.")
