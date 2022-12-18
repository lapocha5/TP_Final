from datetime import datetime
from datetime import timedelta
from Visualización import *
from Actualización import *

import pandas as pd
import yfinance as yf
import sqlite3
import json
import plotly.express as px

def save_ticker_metadata(ticker, st_date, fn_date):
    with open("metadata.json", 'r+') as metadata_file:
        metadata = json.load(metadata_file)

        ticker_exists = False
        for i in metadata["ticker_records"]:
            if i["ticker"] == ticker:
                ticker_exists = True
                i.update({"start_date": st_date, "end_date": fn_date})

        if not ticker_exists:
            new_entry = {"ticker": ticker,
                         "start_date": st_date,
                         "end_date": fn_date}
            metadata["ticker_records"].append(new_entry)

        metadata_file.seek(0)
        json.dump(metadata, metadata_file, indent=4)

def check_ticker_data(ticker):
    with open("metadata.json", 'r+') as metadata_file:
        metadata = json.load(metadata_file)

        for i in metadata["ticker_records"]:
            if i["ticker"] == ticker:
                return i

        return None

def get_ticker_data(ticker, st_date, fn_date):
    error_code = 0

    date_format = "%Y-%m-%d"
    max_years = timedelta(days=365 * 20)

    try:
        start = datetime.strptime(st_date, date_format)
        end = datetime.strptime(fn_date, date_format)
        period = end - start
    except:
        error_code = 2

    if error_code == 0:
        if start >= end or end > datetime.now():
            error_code = 2
        elif period > max_years:
            error_code = 3
        else:
            print("Recuperando información...")
            api_data = yf.Ticker(ticker)
            ticker_data = api_data.history(start=st_date, end=fn_date, debug=False)
            if len(ticker_data) == 0:
                error_code = 1

        if error_code == 0:
            print("Actualizando base...")

            save_ticker_data(ticker, ticker_data)

            save_ticker_metadata(ticker, st_date, fn_date)

    return error_code