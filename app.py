# Lavado Sanitario
# Lavado webApp | Main app container

# ----------------------------------------------------------------------------------------------------------------------
# Library
# ----------------------------------------------------------------------------------------------------------------------
from dash import Dash, html
import dash_labs as dl
import dash_bootstrap_components as dbc

from callbacks import register_callbacks


# ----------------------------------------------------------------------------------------------------------------------
# Main DASH
# ----------------------------------------------------------------------------------------------------------------------
# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

request_path_prefix = None

# Defining the object
app = Dash(__name__, plugins=[dl.plugins.pages], requests_pathname_prefix=request_path_prefix,
           external_stylesheets=[dbc.themes.CERULEAN],  # MINTY, SLATE
           meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}])

# Title of the app
app.title = 'Análisis Lavado Sanitario'
# ----------------------------------------------------------------------------------------------------------------------
# Top menu, items get from all pages registered with plugin.pages
navbar = dbc.Nav(
    [
        dbc.DropdownMenu(
            [
                dbc.DropdownMenuItem('Disasters', href='/'),
                dbc.DropdownMenuItem('Climate Change', href='/climate')
            ],
            nav=True,
            label="Dashboard",
        ),
        dbc.NavItem(dbc.NavLink("Analysis", href='/analysis')),
        dbc.NavItem(dbc.NavLink("About Us", href="/us")),
    ], pills=True, horizontal='end',
)
# ----------------------------------------------------------------------------------------------------------------------
# Dash layout
app.layout = dbc.Container(
    [
        dbc.Row(
            [
                # Logos
                dbc.Col(html.H1([html.Img(src=app.get_asset_url('DS4A.jpg'),
                                          id='logo_ds4a',
                                          style={'height': '40%', 'width': '40%', "margin-left": "20px"},
                                          ),
                                 html.Img(src=app.get_asset_url('Logo_Udjat.PNG'),
                                          id='logo_udjat',
                                          style={'height': '37%', 'width': '37%', "margin-left": "20px"},
                                          )
                                 ], style={'textAlign': 'center'}
                                ), width=2
                        ),
                # Title
                dbc.Col(html.Div([html.H1(children='Udjat', style={'textAlign': 'center'}),
                                  html.H4(children='"Mindfulness of Our World"', style={'textAlign': 'center'}
                                          )], id="Title",
                                 ), width=6
                        ),
                # Tabs
                dbc.Col(html.Div(navbar,
                                 className="one-third column",
                                 id="main_tabs",
                                 style={'textAlign': 'right'}
                                 ), width=4
                        ),
            ],
            id='header', align="center", style={'height': '15%', 'margin-bottom': '20px'}
        ),
        # Line
        dbc.Row([
            html.Hr(style={'borderWidth': "5vh", "width": "100%", "borderColor": "#000000", "opacity": "unset"}),
        ],
            id='line_header', align="center", style={'margin-bottom': '20px'}
        ),
        # Content for different pages
        html.Div(
            children=dl.plugins.page_container,
            id='app-content'
        ),
    ],
    id='mainContainer',
    style={'height': '100vh'}  # "display": "flex", "flex-direction": "column"
)

# Callback
# ----------------------------------------------------------------------------------------------------------------------
register_callbacks(app)

# ----------------------------------------------------------------------------------------------------------------------
# Running the main code
if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0', port=8050)
    #app.run_server(debug=True, port=8050)
