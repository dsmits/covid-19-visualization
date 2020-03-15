# -*- coding: utf-8 -*-
import os

import dash
import dash_html_components as html
import dash_table

import data

DEFAULT_PORT = 8050

df = data.get_data()

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(children=[
    html.H1(children='Covid-19 data visualization'),

    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records')
    )

])


def main():
    port = DEFAULT_PORT
    if os.environ['PORT']:
        port = os.environ['PORT']
        port = int(port)

    app.run_server(debug=True, port=port)


if __name__ == '__main__':
    main()
