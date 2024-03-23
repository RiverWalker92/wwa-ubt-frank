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

def init_dashboard3(server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(
        title='Frankisch Seenland Daten',
        server=server,
        routes_pathname_prefix="/MeanConcentrations/",
        external_stylesheets=[
            "/static/dist/css/styles.css",
            "https://fonts.googleapis.com/css?family=Lato",
        ]
        
    )

    # Load DataFrame
    # Import and clean data (importing csv into pandas)
    df = pd.read_csv("https://raw.githubusercontent.com/Karelknoei92/DashApp/main/All_Lakes_MeanConcentrations.csv")

    #df = df.groupby(['Date', 'Waterlevel', 'Volume', 'Lake'])
    Years=df.Years.unique()
    Lakes = ["GBS", "KBS", "IBS", "AMS"]
    #Names=["Grosser Brombachsee","Kleiner Brombachsee","Igelsbachsee","Altmuehlsee"]

    # Custom HTML layout
    dash_app.index_string = html_layout

    # Create Layout
    
    dash_app.layout=html.Div([

    html.H3("Trends at Different Depths.(select mode for linear regression and what specie to compare. )", style={'text-align': 'center'}),
    html.H3("Lake", style={'text-align': 'left'}),
    dcc.Checklist(id="Lake",
                    options=[{'label': 'Grosser Brombachsee', 'value': 'GBS'},
                        {'label': 'Kleiner Brombachsee', 'value': 'KBS'},
                        {'label': 'Igelsbachsee', 'value': 'IBS'},
                        {'label': 'Altmuhlsee', 'value': 'AMS'},
                        {'label': 'Altmuhlzuleiter', 'value': 'AMSZu'},
                        {'label': 'Nesselbach', 'value': 'Nessel'},
                        {'label': 'Uberleiter', 'value': 'Uber'}],
                        value=["GBS"]
                    ),
    
    html.H3("Chemical Specie", style={'text-align': 'left'}),
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
                            ]
                    ),
    html.H3("Linear regression/Comparison mode (Only the compared variable can have mutiple selections)", style={'text-align': 'left'}),
    dcc.Dropdown(id="Mode",
                    value="LakeComp",
                    multi=False,
                    options=[{'label': 'Lake comparison', 'value': 'LakeComp'},
                            {'label': 'Species comparison', 'value': 'SpecComp'},
                            {'label': 'Trends: Specie comparison', 'value': 'TrendInvSpec'},
                            {'label': 'Trends: Lake comparison', 'value': 'TrendInvLake'}
                           ],
                        style={'float': 'left','margin': 'auto','width': "50%"}
                    ),
    html.Br(),
    html.H3("Month Selection", style={'text-align': 'left','width': "100%"}),      
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
    html.Br(),
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
        Input(component_id='Specie', component_property='value')]
    )
    
    def update_graph(Lake,Month_Trend,Mode,Specie):
        print(Specie)
        print(Lake)
        print(Mode)
        print(Month_Trend)
        print(type(Lake))
        print(type(Specie))
        Lake=list(Lake)
        print(type(Mode))
        print(type(Month_Trend))
        if Mode=='LakeComp':
            df=pd.read_csv("https://raw.githubusercontent.com/Karelknoei92/DashApp/main/All_Lakes_MeanConcentrations.csv")
            dff = df.copy()
            dff["Date"] = pd.to_datetime(df["Date"])
            listx=["Date","Lake"]
            lst=Specie
            listtot=listx+lst
            dff=dff.filter(items=listtot)
            dff=dff.loc[dff['Lake'].isin(Lake)]
            dff=dff.dropna()
            fig = px.line(
                data_frame=dff,
                x='Date',
                y=Specie,
                color='Lake',
                template='plotly_white',
                labels=dict(Date="Years", Value="Value", color="Parameter")
            )

        elif Mode=='SpecComp':
            df=pd.read_csv("https://raw.githubusercontent.com/Karelknoei92/DashApp/main/All_Lakes_MeanConcentrations_2.csv")
            dff = df.copy()
            dff["Date"] = pd.to_datetime(df["Date"])
            listx=["Date","Lake","Specie",'Value']
            dff = dff[dff.columns.intersection(listx)]
            dff=dff.loc[dff['Lake'].isin(Lake)]
            dff=dff.loc[dff['Specie'].isin(Specie)]
            dff=dff.dropna()
            fig = px.line(
                data_frame=dff,
                x='Date',
                y='Value',
                color='Specie',
                template='plotly_white',
                labels=dict(Date="Years", Value="Value", color="Parameter")
            ) 
        elif Mode=='TrendInvSpec':
            df=pd.read_csv("https://raw.githubusercontent.com/Karelknoei92/DashApp/main/All_Lakes_MeanConcentrations_2.csv")
            dff = df.copy()
                      
            dff=dff.loc[dff['Lake'].isin(Lake)]
            dff=dff.loc[dff['Specie'].isin(Specie)]
            listx=["Date","Months","Specie",'Value']
            dff = dff[dff.columns.intersection(listx)]
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
                listx=["Date","Specie",'Value']
                dff = dff[dff.columns.intersection(listx)]
                fig = px.scatter(
                    data_frame=dff,
                    x='Date',
                    y='Value',
                    color='Specie',
                    template='plotly_dark',
                    trendline="ols",
                    labels=dict(Date="Years", Value="Value", color="Parameter")
                )
               
            else:
                listx=["Date","Specie",'Value']
                dff = dff[dff.columns.intersection(listx)]
                fig = px.scatter(
                    data_frame=dff,
                    x='Date',
                    y='Value',
                    color='Specie',
                    template='plotly_dark',
                    trendline="ols",
                    labels=dict(Date="Years", Value="Value", color="Parameter")
                )
        elif Mode=='TrendInvLake':
            df=pd.read_csv("https://raw.githubusercontent.com/Karelknoei92/DashApp/main/All_Lakes_MeanConcentrations.csv")
            dff = df.copy()
            dff["Date"] = pd.to_datetime(df["Date"])
            listx=["Date","Lake","Months"]
            lst=Specie
            listtot=listx+lst
            dff=dff.filter(items=listtot)
            dff=dff.loc[dff['Lake'].isin(Lake)]
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
                    y=Specie,
                    color='Lake',
                    template='plotly_dark',
                    trendline="ols",
                    labels=dict(Date="Years", Value="Value", color="Parameter")
                )
            else:
                fig = px.scatter(
                    data_frame=dff,
                    x='Date',
                    y=Specie,
                    color='Lake',
                    template='plotly_dark',
                    trendline="ols",
                    labels=dict(Date="Years", Value="Value", color="Parameter")
                )        
        return fig
   
