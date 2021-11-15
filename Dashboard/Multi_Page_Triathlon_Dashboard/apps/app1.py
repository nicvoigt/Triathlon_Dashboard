import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

### IN dieser Datei kann man auswählen, welche Ansichten man im Dashboard sehen möchte.

"""
Kombination aus Scatter-Überblick und Detail-Einheit mit Dropdown zur Wahl der Aktivität im Scatter-Überblick

V3:
Der zweite Graph soll aus einem Plot mit zwei y-Achsen bestehen.
Die Inhalte der y-Achsen sollen durch ein Dropdown-Feld gewählt werden.
"""

import json

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import os
import glob
import Garmin_Handler as gh
from scipy import stats
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from Garmin_Handler import Handler as gh


names = ["Radfahren", "Laufen", "Schwimmbadschwimmen", "Freiwasserschwimmen"]



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']



styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}


df0 = pd.read_csv(r"C:\Users\nicoj\netcase\1-Start-UP\Triathlon\Activities.csv")

# TODO: einfügen der Garmin-Handler Funktionen
# TODO: dropdown welcher Einheitstyp gefiltert werden soll
# TODO: Zu der gefilterten EInheit (z.b. laufen) im nächsten dropdown menü auswahlmöglichkeiten anzeigen.

plot_choices = ["Distanz", "Kalorien", "Zeit", "Ø Herzfrequenz", "Maximale Herzfrequenz",
                "Aerober TE", "Ø Geschwindigkeit", "Maximale Geschwindigkeit", "Positiver Höhenunterschied",
                "Negativer Höhenunterschied"]

df0["Zeit"] = pd.to_timedelta(df0["Zeit"])

print(df0["Zeit"])
content_options = plot_choices



detail_options = ['timestamp', "Distanz", 'Geschwindigkeit', 'Höhe', 'Herzfrequenz', 'Temperatur',
                      "latitude", "longitude"]

layout = html.Div([

    html.Div([
            dcc.Dropdown(
                id='name-dropdown', # ÂUswählen, welcher Aktivitätstyp dargestellt wird
                options=[{'label':name, 'value':name} for name in names],
                value = names[0]
                ),
                ],style={'width': '20%', 'display': 'inline-block'}),
    html.Div([
            dcc.Dropdown(
                id='content-dropdown', # ÂUswählen, welcher Performance Indikator dargestellt wird
                options=[{'label':option, 'value':option} for option in content_options],
                value = content_options[0]
                ),
                ],style={'width': '20%', 'display': 'inline-block'}),
    html.Div([
        dcc.Dropdown(
            id='bubble_size',  # ÂUswählen, welcher Indikator für die größe der Bubble verwendet wird.
            options=[{'label': option, 'value': option} for option in content_options],
            value=content_options[0]
        ),
    ], style={'width': '20%', 'display': 'inline-block'}),

    html.Div([dcc.Graph(id="basic-interactions")]),




    """dcc.Graph(
        id='basic-interactions',
        figure=fig
    ),""",

    html.Div(className='row', children=[
        html.Div([
            dcc.Markdown("""
                **Hover Data**

                Mouse over values in the graph.
            """),
            html.Pre(id='hover-data', style=styles['pre'])
        ], className='three columns'),

        html.Div([
            dcc.Markdown("""
                **Click Data**

                Click on points in the graph.
            """),
            html.Pre(id='click-data', style=styles['pre']),
        ], className='three columns')

    ]),

    html.Div([
        dcc.Dropdown(
            id='detail_dropdown1',  # ÂUswählen, welcher Aktivitätstyp dargestellt wird
            options=[{'label': option, 'value': option} for option in detail_options],
            value=detail_options[0]
        ),
    ], style={'width': '20%', 'display': 'inline-block'}),

    html.Div([
        dcc.Dropdown(
            id='detail_dropdown2',  # ÂUswählen, welcher Aktivitätstyp dargestellt wird
            options=[{'label': option, 'value': option} for option in detail_options],
            value=detail_options[0]
        ),
    ], style={'width': '20%', 'display': 'inline-block'}),



html.Div([dcc.Graph(id='output-graph')])


])


#callback for first dropdown to basic interaction graph
#component_id='output-graph', component_property='children'
@app.callback(
    Output('basic-interactions', "figure"),
    [Input("name-dropdown", "value"),
     Input("content-dropdown", "value"),
     Input("bubble_size", "value")
     ]
)
def displac_basic_graph(name_dropdown, content_dropdown, bubble_size):

    # TODO give button to optionally add regression line


    fr = gh.Overview_File_Reader()
    of = fr.read_file()
    #print(of)



    global basic_df     # to work with in this callback
    global name_df      # to load single files
    if name_dropdown == "Schwimmen":
        basic_df = gh.Activity_Handler(of).swim_data()
    elif name_dropdown == "Radfahren":
        basic_df = gh.Activity_Handler(of).bike_data()
    elif name_dropdown == "Laufen":
        basic_df = gh.Activity_Handler(of).run_data()

    name_df = basic_df

    # damit links die alten und rechts die neuen activitaten stehen, wird der index zurückgesetzt
    basic_df.sort_index(ascending=False, inplace = True)
    basic_df.reset_index(drop=True, inplace=True)
    print(0, basic_df.columns)
    test = ['Aktivitätstyp', 'Titel', 'Favorit', 'Datum', 'Zeit']
    cols = basic_df.drop(test, axis=1).columns
    print(1, basic_df)
    basic_df = basic_df[cols].apply(pd.to_numeric, errors='coerce')
    to_drop = []
    for i in basic_df.columns:
        print(basic_df[i].isnull().sum())
        if basic_df[i].isnull().sum() >= len(basic_df) - 5:
            to_drop.append(i)
    # to_drop.extend()

    basic_df.drop(to_drop, axis = 1, inplace = True)
    print(2, basic_df)

    cols = basic_df.columns
    basic_df = basic_df[cols].apply(pd.to_numeric, errors='coerce' )
    print(3, basic_df)
    basic_df.dropna(axis = 0, inplace = True)
    print(4, basic_df)
    basic_df.reset_index(drop=True, inplace=True)
    print(5, basic_df)
    y = pd.to_numeric(basic_df[content_dropdown], errors="coerce")
    y.dropna(inplace = True)
    #basic_df.dropna(inplace=True, axis = 0)



    x = y.index
    #size = basic_df[bubble_size]
    print(basic_df)

    hans = basic_df["Kalorien"]
    print(hans)
    fig = px.scatter(basic_df, x=x, y=str(content_dropdown), size = bubble_size)


    fig.update_layout(clickmode='event+select')
    #fig.update_traces(marker_size=x)

    #TODO if Time is selected on the y-axis, then change the layout of y-axis accordingly.

    return fig
"""
@app.callback(
    Output('hover-data', 'children'),
    [Input('basic-interactions', 'hoverData')])
def display_hover_data(hoverData):
    act_number = hoverData["points"][0]["pointNumber"]
    #print(basic_df.iloc[act_number,:].index)
    Typ = basic_df.iloc[act_number,:]["Aktivitätstyp"]
    titel = basic_df.iloc[act_number,:]["Titel"]
    Datum = basic_df.iloc[act_number,:]["Datum"]
    HF = basic_df.iloc[act_number,:]["Ø Herzfrequenz"]
    Dauer = basic_df.iloc[act_number,:]["Zeit"]
    Geschwindigkeit = basic_df.iloc[act_number,:]["Ø Geschwindigkeit"]




    return_dict = {"Titel":titel,
                   "Datum": str(Datum)}

    #return df0.iloc[act_number,:]
    return_df = pd.DataFrame([titel, Datum], index=["Titel", "Datum"])

    return json.dumps(return_dict, indent=2)

"""
@app.callback(
    Output('output-graph', 'figure'),
    [Input('basic-interactions', 'clickData'), Input('detail_dropdown1', 'value'), Input('detail_dropdown2', 'value')])
def display_click_data(clickData, detail_dropdown1,detail_dropdown2):

    # TODO: change layout of x-Axis from collected timepoints to passed time.
    # TODO: add possibility of changing value to plot on y-Axis:
    #   e.g. plotting heartrate or speed or...
    #   e.g. could also be a click field of plots to plot.

    #TODO add new graph with two y-Axes

    print(clickData)
    act_number = clickData["points"][0]["pointNumber"]
    print(type(name_df.iloc[act_number,:]["Datum"]))

    time_str = str("_") + str(name_df.iloc[act_number, :]["Datum"]).replace("-", "").replace(" ", "-").replace(":", "")
    print((time_str))


    act_str = name_df.iloc[act_number, :]["Aktivitätstyp"]
    file_str = act_str + time_str + ".csv"
    file_str
    #path = r"C:\Users\nicoj\netcase\1-Start-UP\Triathlon\Aktivitaeten_csv"
    # change directory to following folder
    os.chdir(r"C:\Users\nicoj\netcase\1-Start-UP\Triathlon\Aktivitaeten_csv")
    df = pd.read_csv((file_str))
    #print(df.head())
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    if detail_dropdown1=="Geschwindkeit":
        df[detail_dropdown1] = df[detail_dropdown1]*3.6
    if detail_dropdown2 == "Geschwindkeit":
        df[detail_dropdown2] = df[detail_dropdown2] * 3.6
    y1 = df[detail_dropdown1]
    y2 = df[detail_dropdown2]
    # Add traces
    fig.add_trace(
        go.Scatter(x=df.index, y=y1, name=detail_dropdown1),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=df.index, y=y2, name=detail_dropdown2),
        secondary_y=True,
    )

    # Add figure title
    fig.update_layout(
        title_text="Double Y Axis Example"
    )

    # Set x-axis title
    fig.update_xaxes(title_text="xaxis title")

    # Set y-axes titles
    fig.update_yaxes(title_text=detail_dropdown1, secondary_y=False)
    fig.update_yaxes(title_text=detail_dropdown2, secondary_y=True)




    return fig





