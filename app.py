# -*- coding: utf-8 -*-
import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table

import data

_DEFAULT_PORT = 8050
_COLUMNS = ['Date', 'CountryName', 'Confirmed', 'Deaths']

df = data.get_data()

app = dash.Dash(__name__)
server = app.server

app.layout = \
    html.Div(className='app-container',
             children=[
                 html.H1(children='Covid-19 data visualization'),
                 dcc.Markdown(
                     'Visualization of historical data on covid-19 spread and deaths using the Open [COVID-19 Dataset](https://github.com/open-covid-19/data)'),
                 dash_table.DataTable(
                     id='table',
                     columns=[{"name": i, "id": i} for i in _COLUMNS],
                     data=df.to_dict('records'),
                     style_table={
                         'maxHeight': '300px',
                         'overflowY': 'scroll'
                     },
                     filter_action="native",
                     sort_action="native",
                     sort_mode="multi",
                 )

             ])


def main():
    port = os.environ.get('PORT', 8080)
    port = int(port)

    app.run_server(debug=True, port=port)


if __name__ == '__main__':
    main()
