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
import garmin_handler as gh
from scipy import stats
import plotly.graph_objects as go
from plotly.subplots import make_subplots


names = ["Radfahren", "Laufen", "Schwimmbadschwimmen", "Freiwasserschwimmen"]



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

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

app.layout = html.Div([

    html.Div([
            dcc.Dropdown(
                id='name-dropdown', # ÂUswählen, welcher Aktivitätstyp dargestellt wird
                options=[{'label':name, 'value':name} for name in names],
                value = names[0]
                ),
                ],style={'width': '20%', 'display': 'inline-block'}),
    html.Div([
            dcc.Dropdown(
                id='content-dropdown', # ÂUswählen, welcher Aktivitätstyp dargestellt wird
                options=[{'label':option, 'value':option} for option in content_options],
                value = content_options[0]
                ),
                ],style={'width': '20%', 'display': 'inline-block'}),

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
    [Input("name-dropdown", "value"), Input("content-dropdown", "value")]
)
def displac_basic_graph(name_dropdown, content_dropdown):

    # TODO give button to optionally add regression line


    fr = gh.File_Reader()
    of = fr.read_file()
    #print(of)



    global basic_df
    if name_dropdown == "Radfahren":
        basic_df = gh.Activity_Handler().bike_minutes(of)
    elif name_dropdown == "Schwimmen":
        basic_df = gh.Activity_Handler().swim_minutes(of)
    elif name_dropdown == "Laufen":
        basic_df = gh.Activity_Handler().run_minutes(of)

    # damit links die alten und rechts die neuen activitaten stehen, wird der index zurückgesetzt
    basic_df.sort_index(ascending=False, inplace = True)
    basic_df.reset_index(drop=True, inplace=True)




    y = pd.to_numeric(basic_df[content_dropdown], errors="coerce")
    y.dropna(inplace = True)
    x = y.index
    print(y)
    fig = px.scatter(basic_df, x=x, y=y, trendline="ols")
    #slope = stats.linregress(basic_df.index, basic_df["time_ges"]).slope
    #intercept = stats.linregress(basic_df.index, basic_df["time_ges"]).intercept
    #line = slope * x + intercept
    #px.line(line, c="red")
    fig.update_layout(clickmode='event+select')
    fig.update_traces(marker_size=20)

    #TODO if Time is selected on the y-axis, then change the layout of y-axis accordingly.

    return fig

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


@app.callback(
    Output('output-graph', 'figure'),
    [Input('basic-interactions', 'clickData'), Input('detail_dropdown1', 'value'), Input('detail_dropdown2', 'value')])
def display_click_data(clickData, detail_dropdown1,detail_dropdown2 ):

    # TODO: change layout of x-Axis from collected timepoints to passed time.
    # TODO: add possibility of changing value to plot on y-Axis:
    #   e.g. plotting heartrate or speed or...
    #   e.g. could also be a click field of plots to plot.

    #TODO add new graph with two y-Axes

    print(clickData)
    act_number = clickData["points"][0]["pointNumber"]
    print(type(basic_df.iloc[act_number,:]["Datum"]))
    #print(basic_df.iloc[act_number, :]["Datum"])
    time_str = str("_") + str(basic_df.iloc[act_number, :]["Datum"]).replace("-", "").replace(" ", "-").replace(":", "")
    print((time_str))


    act_str = basic_df.iloc[act_number, :]["Aktivitätstyp"]
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




if __name__ == '__main__':
    app.run_server(debug=True)




