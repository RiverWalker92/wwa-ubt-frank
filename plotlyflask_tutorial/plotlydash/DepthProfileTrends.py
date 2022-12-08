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
import statsmodels.api as sm
import statsmodels.formula.api as smf
from dash.dependencies import Input, Output
from .layout import html_layout
from datetime import datetime

def init_dashboard5(server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(
        title='Frankisch Seenland Daten',
        server=server,
        routes_pathname_prefix="/DepthProfileTrends/",
        external_stylesheets=[
            "/static/dist/css/styles.css",
            "https://fonts.googleapis.com/css?family=Lato",
        ]
        
    )

    # Load DataFrame
    # Import and clean data (importing csv into pandas)
    df = pd.read_csv("https://raw.githubusercontent.com/Karelknoei92/DashApp/main/All_Lakes_DepthTrends.csv")

    #df = df.groupby(['Date', 'Waterlevel', 'Volume', 'Lake'])
    Years=df.Years.unique()
    Lakes = ["GBS", "KBS", "IBS", "AMS"]
    #Names=["Grosser Brombachsee","Kleiner Brombachsee","Igelsbachsee","Altmuehlsee"]

    # Custom HTML layout
    dash_app.index_string = html_layout

    # Create Layout
    
    dash_app.layout=html.Div([

    html.H1("Trends at Different Depths", style={'text-align': 'center'}),
    html.Br(),
    dcc.Checklist(id="Lake",
                    options=[{'label': 'Grosser Brombachsee', 'value': 'GBS'},
                        {'label': 'Kleiner Brombachsee', 'value': 'KBS'},
                        {'label': 'Igelsbachsee', 'value': 'IBS'},
                        {'label': 'Altmuhlsee', 'value': 'AMS'}],
                        value=["GBS"],
                        style={'text-align': 'left','margin': 'auto','width': "100%"}
                    ),
    html.Br(),               
    html.H3("Chemical specie", style={'text-align': 'left','margin': 'auto','width': "100%"}),
    dcc.Checklist(id="Specie",
                    value=["Temp"],
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
                            {'label': 'Ratio Total N:Total P (mg/L:mg/L)', 'value': 'RatTN_TP'}
                            ],
                        style={'text-align': 'left','margin': 'auto','width': "100%"}
                    ),
    html.Br(),               
    html.H3("Lake depth", style={'text-align': 'left','margin': 'auto','width': "100%"}),
    dcc.Checklist(id="Depth",
                    value=["Mean","Epi","Hypo"],
                    options=[{'label': 'Mean concentration', 'value': 'Mean'},
                            {'label': 'Epilimnion', 'value': 'Epi'},
                            {'label': 'Hypolimnion', 'value': 'Hypo'}
                            ],
                    style={'text-align': 'left','margin': 'auto','width': "100%"}
                    ),
    html.Br(),               
    html.H3("Mode", style={'text-align': 'left','margin': 'auto','width': "100%"}),
    dcc.Dropdown(id="Mode",
                    value='DepthComp',
                    multi=False,
                    options=[{'label': 'Depth comparison', 'value': 'DepthComp'},
                            {'label': 'Lake comparison', 'value': 'LakeComp'},
                            {'label': 'Species comparison', 'value': 'SpecComp'},
                            {'label': 'Trend Investigation:DepthComp', 'value': 'TrendInvDepth'},
                            {'label': 'Trend Investigation:LakeComp', 'value': 'TrendInvLake'},
                            {'label': 'Trend Investigation:SpecComp', 'value': 'TrendInvSpec'},
                           ],
                        style={'float': 'left','margin': 'auto','width': "50%"}
                    ),
    html.Br(),                                
    dcc.Dropdown(id="Month_Trend",
                    value='None',
                    multi=False,
                    options=[{'label': 'January', 'value': 1},
                            {'label': 'February', 'value': 2},
                            {'label': 'March', 'value': 3},
                            {'label': 'April', 'value': 4},
                            {'label': 'May', 'value': 5},
                            {'label': 'Juni', 'value': 6},
                            {'label': 'July', 'value': 7},
                            {'label': 'Augustus', 'value': 8},
                            {'label': 'September', 'value': 9},
                            {'label': 'October', 'value': 10},
                            {'label': 'November', 'value': 11},
                            {'label': 'December', 'value': 12},
                            {'label': 'All Months', 'value':'None'},
                           ],
                        style={'float': 'left','margin': 'auto','width': "50%"}
                    ),
    html.Br(),
    html.Div(id='output_container', children=[]),
    html.Br(),
    dcc.Graph(id='Lake_waterlevel', figure={})

])
    init_callbacks(dash_app)
    return dash_app.server

def init_callbacks(dash_app):
    @dash_app.callback(
         Output(component_id='Lake_waterlevel', component_property='figure'),
        [Input(component_id='Lake', component_property='value'),
        Input(component_id='Month_Trend', component_property='value'),
        Input(component_id='Mode', component_property='value'),
        Input(component_id='Specie', component_property='value'),
        Input(component_id='Depth', component_property='value')]
    )
    
    def update_graph(Lake,Month_Trend,Mode,Specie,Depth):
        print(Specie)
        print(Lake)
        print(Mode)
        print(Month_Trend)
        print(type(Lake))
        print(type(Specie))
        Lake=list(Lake)
        print(type(Mode))
        print(type(Month_Trend))
        if Mode=='DepthComp':
            df = pd.read_csv("https://raw.githubusercontent.com/Karelknoei92/DashApp/main/All_Lakes_DepthTrends.csv")
            dff = df.copy()
            dff["Date"] = pd.to_datetime(df["Date"])
            listx=["Date","Lake","Depth","Specie",'Value']
            dff = dff[dff.columns.intersection(listx)]
            dff=dff.loc[dff['Lake'].isin(Lake)]
            dff=dff.loc[dff['Specie'].isin(Specie)]
            dff=dff.loc[dff['Depth'].isin(Depth)]
            dff=dff.dropna()
            fig = px.line(
                data_frame=dff,
                x='Date',
                y='Value',
                color='Depth',
                template='plotly_white',
                labels=dict(Date="Years", Value="Value", color="Parameter")
            )
        elif Mode=='LakeComp':
            df = pd.read_csv("https://raw.githubusercontent.com/Karelknoei92/DashApp/main/All_Lakes_DepthTrends.csv")
            dff = df.copy()
            dff["Date"] = pd.to_datetime(df["Date"])
            listx=["Date","Lake","Depth","Specie",'Value']
            dff = dff[dff.columns.intersection(listx)]
            dff=dff.loc[dff['Lake'].isin(Lake)]
            dff=dff.loc[dff['Specie'].isin(Specie)]
            dff=dff.loc[dff['Depth'].isin(Depth)]
            dff=dff.dropna()
            fig = px.line(
                data_frame=dff,
                x='Date',
                y='Value',
                color='Lake',
                template='plotly_white',
                labels=dict(Date="Years", Value="Value", color="Parameter")
                
            )
        elif Mode=='SpecComp':
            df = pd.read_csv("https://raw.githubusercontent.com/Karelknoei92/DashApp/main/All_Lakes_DepthTrends.csv")
            dff = df.copy()
            dff["Date"] = pd.to_datetime(df["Date"])
            listx=["Date","Lake","Depth","Specie",'Value']
            dff = dff[dff.columns.intersection(listx)]
            dff=dff.loc[dff['Lake'].isin(Lake)]
            dff=dff.loc[dff['Specie'].isin(Specie)]
            dff=dff.loc[dff['Depth'].isin(Depth)]
            dff=dff.dropna()
            fig = px.line(
                data_frame=dff,
                x='Date',
                y='Value',
                color='Specie',
                template='plotly_white',
                labels=dict(Date="Years", Value="Value", color="Parameter")
            )
        #Trend Investigations
        elif Mode=='TrendInvDepth':
            df = pd.read_csv("https://raw.githubusercontent.com/Karelknoei92/DashApp/main/All_Lakes_DepthTrends.csv")
            dff = df.copy()
            dff["Date"] = pd.to_datetime(df["Date"])
            listx=["Date","Months","Lake","Depth","Specie",'Value']
            dff = dff[dff.columns.intersection(listx)]
            dff=dff.loc[dff['Lake'].isin(Lake)]
            dff=dff.loc[dff['Specie'].isin(Specie)]
            dff=dff.loc[dff['Depth'].isin(Depth)]
            dff=dff.dropna()

            #Recalculating the dates into years
            date_format = "%m/%d/%Y"
            dff["Date"] = pd.to_datetime(dff["Date"])
            dff["Date"] =dff["Date"].dt.date
            a=datetime.strptime('01/01/2000', date_format).date()
            dates=dff["Date"]-a
            dates=dates.astype(str)
            dates= dates.str.replace(' days', '')
            dff["Date"]=(dates.astype(float)/365)+2000
            #Selecting the months to be viewed
            if Month_Trend!='None':
                dff=dff.loc[dff['Months']==int(Month_Trend)]
                
                fig = px.scatter(
                    data_frame=dff,
                    x='Date',
                    y='Value',
                    color='Depth',
                    template='plotly_white',
                    trendline="ols",
                    labels=dict(Date="Years", Value="Value", color="Parameter")
                )
            else:
                fig = px.scatter(
                    data_frame=dff,
                    x='Date',
                    y='Value',
                    color='Depth',
                    template='plotly_dark',
                    trendline="ols",
                    labels=dict(Date="Years", Value="Value", color="Parameter")
                )
        elif Mode=='TrendInvLake':
            df = pd.read_csv("https://raw.githubusercontent.com/Karelknoei92/DashApp/main/All_Lakes_DepthTrends.csv")
            dff = df.copy()
            dff["Date"] = pd.to_datetime(df["Date"])
            listx=["Date","Months","Lake","Depth","Specie",'Value']
            dff = dff[dff.columns.intersection(listx)]
            dff=dff.loc[dff['Lake'].isin(Lake)]
            dff=dff.loc[dff['Specie'].isin(Specie)]
            dff=dff.loc[dff['Depth'].isin(Depth)]
            dff=dff.dropna()

            #Recalculating the dates into years
            date_format = "%m/%d/%Y"
            dff["Date"] = pd.to_datetime(dff["Date"])
            dff["Date"] =dff["Date"].dt.date
            a=datetime.strptime('01/01/2000', date_format).date()
            dates=dff["Date"]-a
            dates=dates.astype(str)
            dates= dates.str.replace(' days', '')
            dff["Date"]=(dates.astype(float)/365)+2000
            #Selecting the months to be viewed
            if Month_Trend!='None':
                dff=dff.loc[dff['Months']==int(Month_Trend)]
                
                fig = px.scatter(
                    data_frame=dff,
                    x='Date',
                    y='Value',
                    color='Lake',
                    template='plotly_white',
                    trendline="ols",
                    labels=dict(Date="Years", Value="Value", color="Parameter")
                )
            else:
                fig = px.scatter(
                    data_frame=dff,
                    x='Date',
                    y='Value',
                    color='Lake',
                    template='plotly_dark',
                    trendline="ols",
                    labels=dict(Date="Years", Value="Value", color="Parameter")
                )
        elif Mode=='TrendInvSpec':
            df = pd.read_csv("https://raw.githubusercontent.com/Karelknoei92/DashApp/main/All_Lakes_DepthTrends.csv")
            dff = df.copy()
            dff["Date"] = pd.to_datetime(df["Date"])
            listx=["Date","Months","Lake","Depth","Specie",'Value']
            dff = dff[dff.columns.intersection(listx)]
            dff=dff.loc[dff['Lake'].isin(Lake)]
            dff=dff.loc[dff['Specie'].isin(Specie)]
            dff=dff.loc[dff['Depth'].isin(Depth)]
            dff=dff.dropna()

            #Recalculating the dates into years
            date_format = "%m/%d/%Y"
            dff["Date"] = pd.to_datetime(dff["Date"])
            dff["Date"] =dff["Date"].dt.date
            a=datetime.strptime('01/01/2000', date_format).date()
            dates=dff["Date"]-a
            dates=dates.astype(str)
            dates= dates.str.replace(' days', '')
            dff["Date"]=(dates.astype(float)/365)+2000
            #Selecting the months to be viewed
            if Month_Trend!='None':
                dff=dff.loc[dff['Months']==int(Month_Trend)]
                
                fig = px.scatter(
                    data_frame=dff,
                    x='Date',
                    y='Value',
                    color='Specie',
                    template='plotly_white',
                    trendline="ols",
                    labels=dict(Date="Years", Value="Value", color="Parameter")
                )
            else:
                fig = px.scatter(
                    data_frame=dff,
                    x='Date',
                    y='Value',
                    color='Specie',
                    template='plotly_dark',
                    trendline="ols",
                    labels=dict(Date="Years", Value="Value", color="Parameter")
                )
        return fig
   
