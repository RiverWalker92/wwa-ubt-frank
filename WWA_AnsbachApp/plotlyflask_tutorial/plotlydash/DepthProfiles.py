"""Instantiate a Dash app."""
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import numpy as np
import pandas as pd
from datetime import date
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go

from dash.dependencies import Input, Output
from .layout import html_layout


def init_dashboard2(server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(
        title='Frankisch Seenland Daten',
        server=server,
        routes_pathname_prefix="/Depthprofiles/",
        external_stylesheets=[
            "/static/dist/css/styles.css",
            "https://fonts.googleapis.com/css?family=Lato",
        ]
        
    )
    

    # Load DataFrame
    # Import and clean data (importing csv into pandas)
    df = pd.read_csv("https://raw.githubusercontent.com/Karelknoei92/DashApp/main/All_Lakes_Depth_profiles.csv")

    #df = df.groupby(['Date', 'Waterlevel', 'Volume', 'Lake'])
    Years=df.Years.unique()
    Lakes = ["GBS", "KBS", "IBS", "AMS"]
    #Names=["Grosser Brombachsee","Kleiner Brombachsee","Igelsbachsee","Altmuehlsee"]

    # Custom HTML layout
    dash_app.index_string = html_layout

    # Create Layout
    
    dash_app.layout=html.Div([

    
    html.H3("Depth-profiles of Franconian Lake Country (please select year to start)", style={'text-align': 'center'}),
    html.Br(),
    dcc.Dropdown(
        id="Lake",
        value="GBS",
        #multi=False,
        options=[
            {'label': 'Grosser Brombachsee', 'value': 'GBS'},
            {'label': 'Kleiner Brombachsee', 'value': 'KBS'},
            {'label': 'Igelsbachsee', 'value': 'IBS'},
            {'label': 'Altmuhlsee', 'value': 'AMS'}
                ],
                style={'float': 'left','margin': 'auto','width': "60%"}
        ), 
    html.Br(),
    dcc.Dropdown(
        id="Year",
        value="2019",
        options=[{"label": x, "value":x} for x in Years],
                style={'float': 'left','margin': 'auto','width': "60%"}
        ), 
    html.Br(),     
    dcc.Dropdown(
        id="Unit",
        value="Temp",
        multi=False,
        options=[{'label': 'Temperature (degC)', 'value': 'Temp'},
            {'label': 'Oxygen (mg/L)', 'value': 'O2'},
            {'label': 'Total Phosphate (mg/L)', 'value': 'TP'},
            {'label': 'Ortho-Phosphate (mg/L)', 'value': 'PO4'},
            {'label': 'Total Nitrogen(mg/L)', 'value': 'TN'},
            {'label': 'Nitrate (mg/L)', 'value': 'NO3'},
            {'label': 'Ammonium (mg/L)', 'value': 'NH4'},
            {'label': 'Chlorophyl (mg/L)', 'value': 'Chl'},
            {'label': 'Silicate (mg/L)', 'value': 'SiO2'},
            {'label': 'Ratio ortho-P (PO4):Total P (%)', 'value': 'RatPO4_TP'},
            {'label': 'Ratio Ammonium (NH4):Total N (%)', 'value': 'RatNH4_TN'},
            {'label': 'Ratio Total N:Total P (%)', 'value': 'RatTN_TP'}
                ],
                style={'float': 'left','margin': 'auto','width': "60%"}
    ), 
    html.Br(),
    html.Br(),
           
    html.Div(id='output_container', children=[],style={'float': 'left','margin': 'auto','width': "60%"}),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    dcc.Graph(id='Lake_waterlevel', figure={})

])
    init_callbacks(dash_app)
    return dash_app.server

def init_callbacks(dash_app):
    @dash_app.callback(
        [Output(component_id='output_container', component_property='children'),
        Output(component_id='Lake_waterlevel', component_property='figure')],
        [Input(component_id='Lake', component_property='value'),
        Input(component_id='Year', component_property='value'),
        Input(component_id='Unit', component_property='value')
    ]
    )
    
    def update_graph(Lake,Year,Unit):
        #Unit=str(Unit)[2:-2]
        #Lake=str(Lake)
        #Year=int(str(Year)[2:-2])
        print(Unit)
        print(Lake)
        print(Year)
        print(type(Lake))
        print(type(Unit))
        print(type(Year))
        df = pd.read_csv("https://raw.githubusercontent.com/Karelknoei92/DashApp/main/All_Lakes_Depth_profiles.csv")
        container = "The Lake chosen by user was: {}".format(Lake)
        Lake_slctd=Lake
        Year_slctd=Year
        dff = df.copy()
        dff=dff.loc[dff['Years']==Year_slctd]
        dff=dff.loc[dff['Lake']==(Lake_slctd)]

        Months=dff["Months"]
        Conc=dff[Unit]
        Depth=dff["Depth"]
        tickvals=[1,2,3,4,5,6,7,8,9,10,11,12]
        Monthstext=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

        fig = go.Figure(data=go.Heatmap(
            z=Conc,
            x=Months,
            y=Depth,
            colorscale='Viridis'),
            layout=go.Layout(showlegend=True, 
            xaxis=dict(tickvals = tickvals, ticktext = Monthstext)))

        fig.update_layout( yaxis={"title": 'Depth (m)'})
        fig.update_layout( xaxis={"title": 'Months'})
        #fig.update_layout( legend={"title": Unit})
        fig.update_layout( xaxis_nticks=12)
        fig.update_yaxes(autorange="reversed")
        return container, fig
   
