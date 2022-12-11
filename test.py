import sqlite3
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

data_to_plot = pd.read_sql("SELECT Date, Open, High, Low, Close FROM AAPL", conn)

fig = px.line(df, x='Date', y='AAPL.High', title='Time Series with Range Slider and Selectors')

fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
        ])
    )
)
fig.show()
