import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


from app import app
from apps import app1, app2

app.config.suppress_callback_exceptions = True

pages = ["Intensitätsminuten", "Leistungsverlauf"]

app.layout = html.Div([
    dcc.Dropdown(
        id='First_level_dropdown',  # Wählen welche Seite dargestellt wird.
        options=[{'label': page, 'value': page} for page in pages],

    ),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('First_level_dropdown', 'value')])
def display_page(value):
    print(value)

    if value == 'Leistungsverlauf':
        return app1.layout
    elif value == 'Intensitätsminuten':
        return app2.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)