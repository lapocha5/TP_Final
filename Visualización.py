
from datetime import datetime
from datetime import timedelta


import pandas as pd
import yfinance as yf
import sqlite3
import json
import plotly.express as px


def plot_ticker(ticker_name):
        error_code = 0
        try:
            conn = sqlite3.connect("ticker_data.db")
        except:
            error_code = 1

        if error_code == 0:
            data_to_plot = pd.read_sql("SELECT Date, Open, High, Low, Close FROM " + ticker_name, conn)
            fig = px.line(data_to_plot, x='Date', y=['Open','High','Low','Close'], title= 'Serie Temporal con Selectores')
            
            fig.update_layout(
                yaxis_title='Precio de las acciones (USD por Acción)')  

            fig.update_xaxes(
                rangeslider_visible=False,
                    rangeselector=dict(
                        buttons=list([
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
        print("La Database esta en uso, por favor cierre el archivo y intente nuevamente.")

    hist.to_sql(ticker_name, conn, if_exists="replace")
