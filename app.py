# -*- coding: utf-8 -*-
import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
from dash.dependencies import Output, Input

import data
import numpy as np

_DEFAULT_PORT = 8050
_COLUMNS = ['Date', 'CountryName', 'Confirmed', 'Deaths']

df = data.get_data()

app = dash.Dash(__name__)
app.title = 'Coviz - A Covid-19 data visualization'
server = app.server

app.layout = \
    html.Div(className='app-container',
             children=[
                 html.H1(children='Covid-19 data visualization'),
                 dcc.Markdown(
                     'Visualization of historical data on covid-19 spread and deaths using the Open [COVID-19 Dataset](https://github.com/open-covid-19/data)'),
                 dash_table.DataTable(
                     id='coviz-table',
                     columns=[{"name": i, "id": i} for i in _COLUMNS],
                     data=df.to_dict('records'),
                     style_table={
                         'maxHeight': '300px',
                         'overflowY': 'scroll'
                     },
                     filter_action="native",
                     sort_action="native",
                     sort_mode="multi",
                 ),

                 dcc.Graph(
                     id='coviz-graph'
                 ),
                 dcc.Interval('interval-component',
                              interval=1000 * 3600)
             ])


@app.callback(Output('coviz-table', 'data'),
              [Input('interval-component', 'n_intervals')])
def update_data(interval):
    df = data.get_data()
    return df.to_dict('records')


@app.callback(
    Output('coviz-graph', 'figure'),
    [Input('coviz-table', 'derived_virtual_data')])
def display_output(rows):
    filtered_df = pd.DataFrame(rows, columns=_COLUMNS)

    agg = filtered_df.groupby('Date').agg({'Confirmed': 'sum', 'Deaths': 'sum'})

    return {
        'data':
            [
                {'x': agg.index,
                 'y': agg['Confirmed'],
                 'type': 'line',
                 'name': 'Confirmed cases'
                 },
                {'x': agg.index,
                 'y': agg['Deaths'],
                 'type': 'line',
                 'name': 'Deaths'
                 },
                {'x': agg.index,
                 'y': np.log(agg['Confirmed']),
                 'type': 'line',
                 'name': 'Logaritmic confirmed cases'
                 },
                {'x': agg.index,
                 'y': np.log(agg['Deaths']),
                 'type': 'line',
                 'name': 'Logaritmic deaths'
                 }
            ]
    }


def main():
    port = os.environ.get('PORT', 8080)
    port = int(port)

    app.run_server(debug=True, port=port)


if __name__ == '__main__':
    main()
