"""Instantiate a Dash app."""
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import numpy as np
import pandas as pd
from datetime import date
import plotly.express as px  # (version 4.7.0)

from dash.dependencies import Input, Output
from .layout import html_layout


def init_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(
        title='Frankisch Seenland Daten',
        server=server,
        routes_pathname_prefix="/Waterlevels/",
        external_stylesheets=[
            "/static/dist/css/styles.css",
            "https://fonts.googleapis.com/css?family=Lato",
        ]#,
        #csrf_protect=False
    )

    # Load DataFrame
    # Import and clean data (importing csv into pandas)
    df = pd.read_csv("https://raw.githubusercontent.com/Karelknoei92/DashApp/main/Waterlevels.csv")

    #df = df.groupby(['Date', 'Waterlevel', 'Volume', 'Lake'])

    Lakes = ["GBS", "KBS", "IBS", "AMS"]
    #Names=["Grosser Brombachsee","Kleiner Brombachsee","Igelsbachsee","Altmuehlsee"]

    # Custom HTML layout
    dash_app.index_string = html_layout

    # Create Layout
    
    dash_app.layout=html.Div([
    
    
        dcc.Checklist(id="Lake",
                        options=[{'label': 'Grosser Brombachsee', 'value': 'GBS'},
                        {'label': 'Kleiner Brombachsee', 'value': 'KBS'},
                        {'label': 'Igelsbachsee', 'value': 'IBS'},
                        {'label': 'Altmuhlsee', 'value': 'AMS'}],
                        value=["GBS"],
                        labelStyle={'display': 'inline-block'}
                    ),
        html.Br(),
        html.Br(),
        dcc.Dropdown(id="Unit",
                    value="Waterlevel",
                    options=[
                        {'label': 'Waterlevel (m)', 'value': 'Waterlevel'},
                        {'label': 'Volume (m3)', 'value': 'Volume'}
                    ],
                    style={'float': 'left','margin': 'auto','width': "50%"}
                    ),
        html.Br(),
        html.Br(),
              
        html.Div(id='container', children=[]),
        html.Br(),
        dcc.Graph(id='fig', figure={})
    
    ])
    init_callbacks(dash_app)
    return dash_app.server

def init_callbacks(dash_app):
    @dash_app.callback(
        [Output(component_id='container', component_property='children'),
        Output(component_id='fig', component_property='figure')],
        [Input(component_id='Lake', component_property='value'),
            Input(component_id='Unit', component_property='value')]
    )
    
    def update_graph(Lake, Unit):
    #Unit=str(Unit)[1:-1] 
        print(Unit)
        print(Lake)
        print(type(Lake))
        print(type(Unit))
        df = pd.read_csv("https://raw.githubusercontent.com/Karelknoei92/DashApp/main/Waterlevels.csv")
        Lake=list(Lake)
        container = "The Lake chosen by user was: {}".format(Lake)
        dff = df.copy()
        #dff = dff[dff["Lake"] == option_slctd]
        dff=dff.loc[dff['Lake'].isin(Lake)]
        if str(Unit)=='Waterlevel':

            dff=dff.filter(items=['Date','Waterlevel','Lake'])

            fig = px.line(
                data_frame=dff,
                x='Date',
                y='Waterlevel',
                color='Lake',
                template='plotly_white'
            )
        elif str(Unit)=='Volume':
            dff=dff.filter(items=['Date','Volume','Lake'])

            fig = px.line(
                data_frame=dff,
                x='Date',
                y='Volume',
                color='Lake',
                template='plotly_white'
            )
        return container, fig
   
