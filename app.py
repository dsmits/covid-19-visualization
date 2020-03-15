# -*- coding: utf-8 -*-
import dash
import dash_html_components as html
import dash_table

import data

df = data.get_data()

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Covid-19 data visualization'),

    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records')
    )

])

if __name__ == '__main__':
    app.run_server(debug=True)
