import dash
import dash_core_components as dcc
import dash_html_components as html
import glob, os
import pandas as pd

#change directory to following folder
os.chdir(r"C:\Users\nicoj\netcase\1-Start-UP\Triathlon\Aktivitaeten_csv")

directory_link = r"C:\Users\nicoj\netcase\1-Start-UP\Triathlon\Aktivitaeten_csv"

#initiate list with activities:
act_list = []
for file in glob.glob("*.*"):
    if str(file).count(".csv")==1:
        act_list.append(file)



app = dash.Dash()


Laufen_dates = []
Bike_dates = []
SSwim_dates = []
FSwim_dates = []
for act in act_list:
    if act.count("Laufen")==1:
        #fill laufen_dates with the date of the current activity
        Laufen_dates.append(act.split("_")[1])
    if act.count("Radfahren")==1:
        #fill bike_dates with the date of the current activity
        Bike_dates.append(act.split("_")[1])
    if act.count("Schwimmbadschwimmen")==1:
        #schwimmbadschwimmen
        SSwim_dates.append(act.split("_")[1])
    if act.count("Freiwasserschwimmen")==1:
        FSwim_dates.append(act.split("_")[1])


Act_Dict = {'Radfahren': Bike_dates,
             'Laufen': Laufen_dates,
             "Schwimmbadschwimmen" : SSwim_dates,
            "Freiwasserschwimmen" : FSwim_dates
            }

names = list(Act_Dict.keys())
nestedOptions = Act_Dict[names[0]]

app.layout = html.Div(
    [
        html.Div([
        dcc.Dropdown(
            id='name-dropdown', # choose activity type
            options=[{'label':name, 'value':name} for name in names],
            value = list(Act_Dict.keys())[0]
            ),
            ],style={'width': '20%', 'display': 'inline-block'}),
        html.Div([
        dcc.Dropdown(
            id='opt-dropdown', # chose single activity
            ),
            ],style={'width': '20%', 'display': 'inline-block'}
        ),
        html.Div([
        dcc.Dropdown(
            id='plot-dropdown', # chose property to plot
            ),
            ],style={'width': '20%', 'display': 'inline-block'}
        ),

        html.Hr(),
        html.Div(id='output-graph')
    ]
)

@app.callback(
    dash.dependencies.Output('opt-dropdown', 'options'),
    [dash.dependencies.Input('name-dropdown', 'value')]
)
def update_date_dropdown(name):
    global test
    test = name
    return [{'label': i, 'value': i} for i in Act_Dict[name]]

@app.callback(
    dash.dependencies.Output('plot-dropdown', 'options'),
    [dash.dependencies.Input('opt-dropdown', 'value')]
)
def choose_plot_content(activity):
    print("ACTIVITY:", activity)
    columns = list(pd.read_csv(os.path.join(directory_link + "/" + test + "_" + activity + "_" + ".csv"), index_col = 0).columns)
    print("COLUMNS:", columns)
    global activity_to_plot
    activity_to_plot = activity
    return [{'label': i, 'value': i} for i in columns]

@app.callback(
    dash.dependencies.Output(component_id='output-graph', component_property='children'),
    [dash.dependencies.Input(component_id='plot-dropdown', component_property='value')]
)
def update_value(input_data):
    print("INPUT_DATA", input_data)
    print("TYPE_INPUT_DATA:", type(input_data))
    print("TEST", test)
    print("ACTIVITY_TO_PLOT:", activity_to_plot)

    df = pd.read_csv(os.path.join(directory_link + "/" + test + "_" + activity_to_plot + "_" + ".csv"))

    return dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': df.index, 'y': df[input_data]*3.6, 'type': 'line', 'name': input_data},
            ],
            'layout': {
                'title': input_data
            }
        }
    )



if __name__ == '__main__':
    app.run_server(debug=True)
