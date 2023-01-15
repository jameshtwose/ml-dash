from dash import Dash, dcc, html
import dash_bootstrap_components as dbc

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "30rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "30rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

# sidebar = html.Div(
#     [
#         html.H2("Machine Learning Dashboard", className="display-4"),
#         html.Hr(),
#         html.P(
#             """Upload your data in csv format and an EDA will be run as
#             well as the main Machine Learning analysis, with comparison metrics.""", 
#             className="lead"
#         ),
#         html.Hr(),
#         dcc.Dropdown(options=["ASN"], 
#                      value="ASN",
#                      multi=False, 
#                      id='bank-string-dropdown'),
#         html.Hr(),
#         dcc.Upload(html.Button('Upload File'), id='upload-data', multiple=True),
#         html.Hr(),
#         dbc.Nav(
#             [
#                 dbc.NavLink("Home/ Descriptives", href="/", active="exact"),
#                 dbc.NavLink("Bar Plots", href="/page-1", active="exact"),
#                 dbc.NavLink("Time Series Plots", href="/page-2", active="exact"),
#             ],
#             vertical=True,
#             pills=True,
#         ),
#         html.Hr(),
#         html.Div(
#             [html.Img(src=r'assets/logo.png', alt='logo', width=80)],
#             style = {'textAlign': 'center'}),       
#         html.Div(
#             [html.A(children="Created by James Twose",
#                 href="https://services.jms.rocks",
#                 style={'color': "#5f4a89"})],
#                 style = {'textAlign': 'center',
#                             'color': "#5f4a89",
#                             'marginTop': 40,
#                             'marginBottom': 40}),
#     ],
#     style=SIDEBAR_STYLE,
# )

def sidebar(column_list):
    return html.Div(
    [
        html.H2("Machine Learning Dashboard", className="display-4"),
        html.Hr(),
        html.P(
            """Upload your data in csv format and an EDA will be run as
            well as the main Machine Learning analysis, with comparison metrics.""", 
            className="lead"
        ),
        html.Hr(),
        dcc.Dropdown(options=column_list, 
                    #  value=column_list[0],
                     multi=False, 
                     id='bank-string-dropdown'),
        html.Hr(),
        dcc.Upload(html.Button('Upload File'), id='upload-data', multiple=True),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Home/ Descriptives", href="/", active="exact"),
                dbc.NavLink("Bar Plots", href="/page-1", active="exact"),
                dbc.NavLink("Time Series Plots", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
        html.Hr(),
        html.Div(
            [html.Img(src=r'assets/logo.png', alt='logo', width=80)],
            style = {'textAlign': 'center'}),       
        html.Div(
            [html.A(children="Created by James Twose",
                href="https://services.jms.rocks",
                style={'color': "#5f4a89"})],
                style = {'textAlign': 'center',
                            'color': "#5f4a89",
                            'marginTop': 40,
                            'marginBottom': 40}),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div([html.Div(id='output-data-upload')], id="page-content", 
                   style=CONTENT_STYLE)