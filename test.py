import sqlite3
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

conn = sqlite3.connect("ticker_data.db")

data_to_plot = pd.read_sql("SELECT Date, Open, High, Low, Close FROM AAPL", conn)
fig = go.Figure(data=[go.Candlestick(x=data_to_plot['Date'],
                open=data_to_plot['Open'],
                high=data_to_plot['High'],
                low=data_to_plot['Low'],
                close=data_to_plot['Close'])])

fig.show()


