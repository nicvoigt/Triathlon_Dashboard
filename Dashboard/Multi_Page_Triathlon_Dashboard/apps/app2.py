import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import Garmin_Handler.Handler as gh
import pandas as pd
import dash
import plotly.express as px
import plotly.graph_objects as go

from app import app

global of
of = gh.Overview_File_Reader().read_file()
#of = gh.Activity_Handler(of).bike_data()

betrachtungszeitraum = ["Woche", "Monat", "Jahr"]
split_options = ["Kein Split", "Gestapelter Split", "Split nebeneinander"]
layout = html.Div([
    html.Div(
    dcc.Textarea(
        id='textarea-example',
        value='Darstellung der Aktivitätsminuten \n Auswahl des Betrachtungszeitraums:',
        style={'width': '100%', 'height': 50, "fontSize" : 20, 'font-weight': 'bold'},
        readOnly=True, cols = 2
    )
    ),
html.Div([
    html.Button('Grafisch', id='plot_button', n_clicks=0),
    html.Button('Tabular', id='table_button', n_clicks=0),
    dcc.Dropdown(id = "choose_split",
                 options = [{'label': split, 'value': split} for split in split_options])

        ]),

    dcc.Dropdown(
        id='horizont',
        options=[
            {'label': bz, 'value': bz} for bz in betrachtungszeitraum
        ]
    ),

    html.Div([dcc.Graph(id="plot")]),
    html.Div(id="table"),
    html.Div(id='app-1-display-value'),
    dcc.Link('Go to App 2', href='/apps/app2')
])



@app.callback(
    Output('app-1-display-value', 'children'),
    [Input('app-1-dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)


@app.callback(
    Output("plot", "figure"),
    [Input("horizont", "value"),
     Input("plot_button", "n_clicks"),
     Input("table_button", "n_clicks"),
     Input("choose_split", "value")
     ])
def select_plot(horizon, bnt1, btn2, choose_split):

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]




    if horizon == "Woche":
        if choose_split=="kein Split":
            of2 = pd.DataFrame(gh.Activity_Handler(of).weekly_minutes_total())
            of2["Woche"] = of2.index
            of2.reset_index(drop=True, inplace=True)

        elif choose_split == "Gestapelter Split":
            of2 = pd.DataFrame(gh.Activity_Handler(of).weekly_minutes_split())

            of2["Woche"] = of2.index
            # of2["Woche"] = of2["Woche"].str.split(" ", expand = True)[0]

            of2.reset_index(drop=True, inplace=True)

            fig = px.bar(of2, x=of2[horizon], y="Total time in Minutes", color="Aktivitätstyp", title="Long-Form Input")
            fig.update_layout(
                autosize=True)
            return fig
        elif choose_split ==  "Split nebeneinander":
            of2 = pd.DataFrame(gh.Activity_Handler(of).weekly_minutes_split())

            of2["Woche"] = of2.index

            of2.reset_index(drop=True, inplace=True)

            runs = of2[of2["Aktivitätstyp"]=="Laufen"]
            fitti = of2[of2["Aktivitätstyp"]=="Fittnessstudio und -geräte"]
            swim = of2[of2["Aktivitätstyp"] == "Schwimmen"]
            bike = of2[of2["Aktivitätstyp"] == "Radfahren"]


            fig = go.Figure(data=[
                go.Bar(name='Schwimmen', x=of2["Woche"], y=swim["Total time in Minutes"]),
                go.Bar(name='Radfahren', x=of2["Woche"], y=bike["Total time in Minutes"]),
                go.Bar(name='Laufen', x=of2["Woche"], y=runs["Total time in Minutes"]),
                go.Bar(name='Fitti', x=of2["Woche"], y=fitti["Total time in Minutes"])
            ])
            # Change the bar mode
            #fig.update_layout(barmode='group', autosize=True)
            #fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
            #                  marker_line_width=1.5, opacity=0.6)
            fig.update_layout(barmode='group', autosize=True )
            print(runs.tail())
            return fig


    elif horizon == "Monat":
        if choose_split=="kein Split":
            of2 = pd.DataFrame(gh.Activity_Handler(of).monthly_minutes_total())
            print(of2.head())
            of2["Monat"] = of2.index
            of2.reset_index(drop=True, inplace=True)

        elif choose_split == "Split":


            pass
            #fig = go.Figure(data=[
            #    go.Bar(name='SF Zoo', x=animals, y=[20, 14, 23]),
            #    go.Bar(name='LA Zoo', x=animals, y=[12, 18, 29])
            #])
            # Change the bar mode
            #fig.update_layout(barmode='group')
            #fig.show()

    if "plot_button.n_clicks" in changed_id:
        fig = px.bar(of2, x=of2[horizon], y="Total time in Minutes", title="Long-Form Input")
        fig.update_layout(
            autosize=True)

    elif "table_button.n_clicks" in changed_id:
        fig = px.bar(of2, x=of2[horizon], y="Total time in Minutes",color = "medal", title="Long-Form Input")
        fig.update_layout(
            autosize=False,
            width=10,
            height=10)

    return fig


@app.callback(
    Output("table", "children"),
    [Input("horizont", "value"),
     Input("plot_button", "n_clicks"),
     Input("table_button", "n_clicks")
     ])
def select_table(value, bn1, bn2):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    print(value)


    if value == "Woche":
        of2 = pd.DataFrame(gh.Activity_Handler(of).weekly_minutes_total())
        of2["Woche"] = of2.index
        of2.reset_index(drop=True, inplace=True)


    elif value == "Monat":
        of2 = pd.DataFrame(gh.Activity_Handler(of).monthly_minutes_total())
        of2["Monat"] = of2.index
        of2.reset_index(drop=True, inplace=True)


    if "plot_button.n_clicks" in changed_id:
        return

    elif "table_button.n_clicks" in changed_id:

        return dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in of2.columns],
        data=of2.to_dict('records'))

