




import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import os


directory_link = r"C:\Users\nicoj\netcase\1-Start-UP\Triathlon\Aktivitaeten_csv"




app = dash.Dash()

app.layout = html.Div(children=[
    html.Div(children='''
        Symbol to graph:
    '''),
    dcc.Input(id='input', value='', type='text'),
    dcc.Input(id='input_2', value='', type='text'),

    dcc.Dropdown(
        id='demo_dropdown',
        options=[
            {'label': 'Radfahren', 'value': 'Radfahren'},
            {'label': 'Laufen', 'value': 'Laufen'},
            {'label': 'Schwimmen', 'value': 'Schwimmen'}
        ],
        value='Radfahren'),
    dcc.Dropdown(
        id='demo_dropdown_2',
        options=[
            {'label': 'Lauf', 'value': '_20200524-121205_'},
            {'label': 'Rad', 'value': '_20200520-122030_'},

        ],
        value='Lauf'),



    html.Div(id='output-graph'),
])


@app.callback(
    Output(component_id='output-graph', component_property='children'),
    [Input(component_id='demo_dropdown', component_property='value'),
    Input(component_id='demo_dropdown_2', component_property='value')
     ]
)
def update_value(demo_dropdown_data,demo_dropdown_data_2):
    demo_dropdown_data
    date = demo_dropdown_data_2


    df = pd.read_csv(os.path.join(directory_link + "/" +  demo_dropdown_data + date +  ".csv"))


    return dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': df.index, 'y': df.latitude, 'type': 'line', 'name': demo_dropdown_data},
            ],
            'layout': {
                'title': demo_dropdown_data
            }
        }
    )

if __name__ == '__main__':
    app.run_server(debug=True)