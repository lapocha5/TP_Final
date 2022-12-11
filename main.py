from datetime import datetime
from datetime import timedelta

import pandas as pd
import yfinance as yf
import sqlite3
import json
import plotly.graph_objects as go
import plotly.express as px

def plot_ticker(ticker_name):
    error_code = 0
    try:
        conn = sqlite3.connect("ticker_data.db")
    except:
        error_code = 1

    if error_code == 0:
        data_to_plot = pd.read_sql("SELECT Date, Open, High, Low, Close FROM " + ticker_name, conn)
        fig = px.line(data_to_plot, x='Date', y='High', title= 'Time Series with Range Slider and Selectors')

        fig.update_layout(
            yaxis_title='Stock Price (USD per Shares)')  

        fig.update_xaxes(
            rangeslider_visible=True,
                rangeselector=dict(
                    buttons=list([
                        dict(count=1, label="15m", step="minute", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(count=1, label="YTD", step="year", stepmode="todate"),
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(step="all")
                    ])
                )
            )
        fig.show()

def save_ticker_data(ticker_name, hist):
    conn = None
    try:
        conn = sqlite3.connect("ticker_data.db")
    except:
        print("Database is in use (I guess?), please close the file and try again.")

    hist.to_sql(ticker_name, conn, if_exists="replace")


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
            print("Fetching data...")
            api_data = yf.Ticker(ticker)
            ticker_data = api_data.history(start=st_date, end=fn_date, debug=False)
            if len(ticker_data) == 0:
                error_code = 1

        if error_code == 0:
            print("Updating database...")

            save_ticker_data(ticker, ticker_data)

            save_ticker_metadata(ticker, st_date, fn_date)

    return error_code


def error_handling(error_code):
    if error_code == 1:
        print("Ticker is invalid, please verify and enter again.")
    elif error_code == 2:
        print("Dates are invalid, please verify and enter again.")
    elif error_code == 3:
        print("The range requested exceeds the capabilities of this software, please enter a shorter date range.")


exit_command = False

while not exit_command:
    user_command = input("Choose between 'get', 'check', and 'display' a ticker\n").lower()

    if user_command == 'get':
        ticker = input("Enter ticker: ").upper()
        st_date = input("Enter start date (YYYY-MM-DD): ")
        fn_date = input("Enter final date (YYYY-MM-DD): ")

        get_error_code = get_ticker_data(ticker, st_date, fn_date)
        if get_error_code == 1:
            print("Ticker is invalid, please verify and enter again.")
        elif get_error_code == 2:
            print("Dates are invalid, please verify and enter again.")
        elif get_error_code == 3:
            print("The range requested exceeds the capabilities of this software, please enter a shorter date range.")

    elif user_command == 'check':
        ticker = input("Enter ticker: ").upper()
        ticker_meta_data = check_ticker_data(ticker)

        if ticker_meta_data is None:
            print("No data has been gathered for that ticker yet.")
        else:
            print("Start date: " + ticker_meta_data["start_date"])
            print("End date: " + ticker_meta_data["end_date"])

    elif user_command == 'display':
        ticker = input("Enter ticker: ").upper()
        ticker_meta_data = check_ticker_data(ticker)

        if ticker_meta_data is None:
            print("No data has been gathered for that ticker yet.")
        else:
            plot_ticker(ticker)

    elif user_command == 'exit':
        exit_command = True

    else:
        print("Not a valid command.")

print("Thank you for using our services, have a great day.")
