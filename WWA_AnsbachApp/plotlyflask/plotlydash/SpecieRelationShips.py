"""Instantiate a Dash app."""
import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px  # (version 4.7.0)
from dash.dependencies import Input, Output
from .layout import html_layout


def init_dashboard4(server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(
        title='Frankisch Seenland Daten',
        server=server,
        routes_pathname_prefix="/SpecieRelations/",
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
    #Names=["Grosser Brombachsee","Kleiner Brombachsee","Igelsbachsee","Altmuehlsee"]

    # Custom HTML layout
    dash_app.index_string = html_layout

    # Create Layout
    
    dash_app.layout=html.Div([

    html.Br(),
    html.H3("Lake", style={'text-align': 'left'}),
    dcc.Checklist(id="Lake",
                         options=[{'label': 'Grosser Brombachsee', 'value': 'GBS'},
                        {'label': 'Kleiner Brombachsee', 'value': 'KBS'},
                        {'label': 'Igelsbachsee', 'value': 'IBS'},
                        {'label': 'Altmuhlsee', 'value': 'AMS'},
                        {'label': 'Altmuhlzuleiter', 'value': 'AMSZu'},
                        {'label': 'Nesselbach', 'value': 'Nessel'},
                        {'label': 'Uberleiter', 'value': 'Uber'}],
                        value=["GBS"],
                        style={'float': 'left','margin': 'auto','width': "100%"}
                    ),
    html.Br(),               
    html.H3("x-axis input (select 1)", style={'text-align': 'left'}),
    dcc.Dropdown(id="XAxis",
                    multi=False,
                    value="Temp",
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
                        style={'float': 'left','margin': 'auto','width': "50%"}
                    ),
    html.Br(),               
    html.H3("Y-axis input (select 1 or more)", style={'text-align': 'left'}),
    dcc.Checklist(id="YAxis",
                    value=["O2"],
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
                        style={'float': 'left','margin': 'auto','width': "100%"}
                    ),
    html.Br(),               
    html.H3("Modus", style={'text-align': 'left','margin': 'auto','width': "100%"}),
    html.Br(),
    dcc.Dropdown(id="Mode",
                    value="LakeComp",
                    multi=False,
                    options=[{'label': 'Lake comparison', 'value': 'LakeComp'},
                            {'label': 'Species comparison', 'value': 'SpecComp'}
                           ],
                        style={'float': 'left','margin': 'auto','width': "100%"}
                    ),
    html.Br(),  
    html.H3("Month selection", style={'text-align': 'left','margin': 'auto','width': "100%"}),     
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
                        style={'float': 'left','margin': 'auto','width': "100%"}
                    ),
    html.Br(),
    html.Br(),
    html.Br(),
    dcc.Graph(id='Lake_waterlevel', figure={})

])
    init_callbacks(dash_app)
    return dash_app.server

def init_callbacks(dash_app):
    @dash_app.callback(
    Output(component_id='Lake_waterlevel', component_property='figure'),
    [Input(component_id='Lake', component_property='value'),
    Input(component_id='XAxis', component_property='value'),
    Input(component_id='YAxis', component_property='value'),
    Input(component_id='Mode', component_property='value'),
    Input(component_id='Month_Trend', component_property='value')]
    )
    
    def update_graph(Lake,XAxis,YAxis,Mode,Month_Trend):
        if  Mode=='LakeComp':
            df=pd.read_csv("https://raw.githubusercontent.com/Karelknoei92/DashApp/main/All_Lakes_MeanConcentrations.csv")
            dff = df.copy()
            Lake=list(Lake)
            listx=['Lake','Months']
            lst=YAxis+[XAxis]
            listtot=listx+lst
            listtot=list(set(listtot))
            dff=dff.filter(items=listtot)
            dff=dff.loc[dff['Lake'].isin(Lake)]
            dff=dff.dropna()
            if Month_Trend!='None':
                dff=dff.loc[dff['Months']==int(Month_Trend)]
                fig = px.scatter(
                    data_frame=dff,
                    x=str(XAxis),
                    y=YAxis,
                    color='Lake',
                    template='plotly_white',
                    trendline="ols"
                )
            else:         
                fig = px.scatter(
                    data_frame=dff,
                    x=str(XAxis),
                    y=YAxis,
                    color='Lake',
                    template='plotly_white',
                    trendline="ols",
                    )
        elif  Mode=='SpecComp':
            df=pd.read_csv("https://raw.githubusercontent.com/Karelknoei92/DashApp/main/All_Lakes_MeanConcentrations_2.csv")
            dff = df.copy()
            listx=['Lake','Months','Specie','Value']
            dff = dff[dff.columns.intersection(listx)]
            dff=dff.loc[dff['Lake'].isin(Lake)]
            X=dff.loc[dff['Specie']==str(XAxis)]
            X=X['Value']
            X=X.append([X]*(len(YAxis)-1),ignore_index=False)     
            dff=dff.loc[dff['Specie'].isin(YAxis)]
            X.index = dff.index     
            dff.insert(0, str(XAxis),X ,allow_duplicates = False)
            dff=dff.dropna()
            if Month_Trend!='None':
                dff=dff.loc[dff['Months']==int(Month_Trend)]
                listx=[str(XAxis),'Specie','Value']
                dff = dff[dff.columns.intersection(listx)]
                fig = px.scatter(
                    data_frame=dff,
                    x=XAxis,
                    y='Value',
                    color='Specie',
                    template='plotly_white',
                    trendline="ols"
                )
            else:
                listx=[str(XAxis),'Specie','Value']
                dff = dff[dff.columns.intersection(listx)]          
                fig = px.scatter(
                    data_frame=dff,
                    x=XAxis,
                    y='Value',
                    color='Specie',
                    template='plotly_white',
                    trendline="ols",
                    )   
        return fig
   
