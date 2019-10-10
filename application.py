import _plotly_future_
from _plotly_future_ import v4_subplots

# Import Dash and Plotly components/packages

import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly
from dash.dependencies import Input, Output, State
import dash_table as dt
import plotly.graph_objs as go
from plotly.subplots import make_subplots



# Importing custom function winRecords and binaryFTR

from winRecords import winRecords, binaryFTR
import pandas as pd
import numpy as np

# Read Files into appropriate data type - i.e. dataFrame or array, list, dict, etc.

tabdata = pd.read_csv("serieA/serieA_season-1819.csv") #DataFrame
resD = binaryFTR(pd.read_csv("serieA/serieA_season-1819.csv"), 'FTR') #
yData1 = (winRecords(pd.read_csv("serieA/serieA_season-1617.csv"), 'SerieA_16_17', 'FTR'))
yData2 = (winRecords(pd.read_csv("serieA/serieA_season-1718.csv"), 'SerieA_17_18', 'FTR'))
yData3 = (winRecords(pd.read_csv("serieA/serieA_season-1819.csv"), 'SerieA_18_19', 'FTR'))
seasonsLabels = ['2016/17', '2017/18', '2018/19']
pieData17 = [yData2[0], yData2[1], yData2[2]]
pieData18 = [yData3[0], yData3[1], yData3[2]]
catLabels = ['Home wins', 'Away wins', 'Draws']

# Dataset for Pie chart (slider)
dff = pd.read_csv('serieA/saa.csv')

# Building the Dash app

app = dash.Dash(__name__)
app.title = 'Serie A Stats Dashboard'

app.scripts.config.serve_locally = True
app.css.config.serve_locally = True
app.config.suppress_callback_exceptions = True
colors = {
    'background': '#FFFFFF',
    'text': '#000000'
}
app.layout = html.Div([

    html.Div([

        html.H1(
        children='Win Distributions in Serie A by year',
        style={
            'textAlign': 'center',
            'color': colors['text'],
            'font-family': 'Gill Sans'
        }
        ),

        html.Div([
            dcc.Location(id='url', refresh=False),
            html.Div(id='page-content')
        ]),
    

]),



    #html.Div([

        #dt.DataTable(

         #   id='table',
          #  columns=[{"name": i, "id": i} for i in tabdata.columns],
           # data=tabdata.to_dict('records'),
        #)


    #]),
    
    html.Div(id='page-1-content'),
    html.Br(),
    dcc.Link('Season-specific analysis', href='/page-2'),
    html.Br(),
    dcc.Link('Overview Analysis', href='/'),
])

index_page = html.Div([
    dcc.Link('Season-specific analysis', href='/page-1'),
    html.Br(),
    dcc.Link('Go to Page 2', href='/page-2'),

    html.Div([

        html.Div([html.H1("Overview")], style={"textAlign": "center"}),
            dcc.Graph(id="my-graph"),
            html.Div([dcc.Slider(id='season', min=1, max=4, value=3,
                                marks={1: "2015/16", 2: "2016/17", 3: "2017/18", 4: "2018/19"})],
                    style={'textAlign': "center", "margin": "30px", "padding": "10px", "width": "65%", "margin-left": "auto",
                            "margin-right": "auto"}),
        ], className="container")


])

page_1_layout = html.Div([
    html.Div([
                
                html.Div(id='page-2-content'),
                html.Br(),
                dcc.Link('Go to Page 2', href='/page-2'),
                html.Br(),
                dcc.Link('Overview Analysis', href='/'),
            
                dcc.Tabs(id="tabs", value='stab-1', children=[
                    dcc.Tab(id = 'tab_1',label='2017/18', value='tab-1'),
                    dcc.Tab(id = 'tab_2',label='2018/19', value='tab-2'),
                ])
                ]),
                html.Div(id='tabs-content'),
        ]),

@app.callback(dash.dependencies.Output('page-1-content', 'children'),
              [dash.dependencies.Input('page-1-dropdown', 'value')])
def page_1_dropdown(value):
    return 'You have selected "{}"'.format(value)


page_2_layout = html.Div([
    html.H1('Page 2'),
    dcc.RadioItems(
        id='page-2-radios',
        options=[{'label': i, 'value': i} for i in ['Orange', 'Blue', 'Red']],
        value=winRecords(pd.read_csv("serieA/serieA_season-1819.csv"), 'SerieA_18_19', 'FTR')
    ),
    html.Div([
    html.Div(id='target'),
    dcc.Input(id='input', type='text', value=''),
    html.Button(id='submit', n_clicks=0, children='Save')
    ]),

    html.Div(id='page-2-content'),
    html.Br(),
    dcc.Link('Season-specific analysis', href='/page-1'),
    html.Br(),
    dcc.Link('Overview Analysis', href='/')
])

# Callback for input value (ML)
@app.callback(Output('target', 'children'), [Input('submit', 'n_clicks')],
              [State('input', 'value')])
def callback(n_clicks, state):
    arrayN = np.array(state.split(","))

    return "For your Machine learning test, please enter IN THIS ORDER (separated by commas), Home Team name, Away Team Name, Home Shots, Away Shots,Home Shots on Target, Away Shots on Target, Home Fouls, Away Fouls, Home Corners, Away Corners, Home Yellow Cards, Away Yellow Cards, Home Red Cards, Away Red Cards: {}".format(arrayN)

@app.callback(dash.dependencies.Output('page-2-content', 'children'),
              [dash.dependencies.Input('page-2-radios', 'value')])
def page_2_radios(value):
    return 'You have selected "{}"'.format(value)




# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    else:
        return index_page
    # You could also return a 404 "URL not found" page here


@app.callback(
    
     Output('tabs-content', 'children'),
     [Input('tabs', 'value')])              

def render_content(tab):

    if tab == 'tab-1':
        return html.Div(
            [
                html.Div([
                    dcc.Graph(
                            id='yData1_0-plot',
                            figure={
                                    'data': [
                                            go.Pie(labels=list(catLabels), values=list(pieData17))],
                                            'layout': go.Layout(
                                                    title = 'Pie Chart',
                                                    hovermode='closest'
                                                    )
                                            }
                            )], style={'width':'100%','display':'inline-block','font-family':'Arial Black, Arial'}),
            
                html.Div([
                    dcc.Graph(id='dt2-plot',
                            figure={
                                
                                'data': [
                                    {'x': [2017], 'y': [yData2[0]], 'type': 'bar', 'name': 'Home Wins'},
                                    {'x': [2017], 'y': [yData2[2]], 'type': 'bar', 'name': 'Draws'},
                                    {'x': [2017], 'y': [yData2[1]], 'type': 'bar', 'name': 'Away Wins'}
                                ],
                                'layout': {
                                    'title' : 'Bar graph showing distribution',
                                    'plot_bgcolor': colors['background'],
                                    'paper_bgcolor': colors['background'],
                                    'font': {
                                        'color': colors['text']
                                    }
                                }
                            }
                            )], style={'width':'100%','display':'inline-block'})
            ])

    elif tab == 'tab-2':
        return html.Div(
            [
            html.Div([
                    dcc.Graph(
                            id='yData1_0-plot',
                            figure={
                                    'data': [
                                            go.Pie(labels=list(catLabels), values=list(pieData18))],
                                            'layout': go.Layout(
                                                    title = 'Pie Chart',
                                                    hovermode='closest'
                                                    )
                                            }
                            )], style={'width':'100%','display':'inline-block', 'font-family':'Georgia'}),
            html.Div([
                    dcc.Graph(id='dt2-plot',
                            figure={
                                
                                'data': [
                                    {'x': [2018], 'y': [yData3[0]], 'type': 'bar', 'name': 'Home Wins'},
                                    {'x': [2018], 'y': [yData3[2]], 'type': 'bar', 'name': 'Draws'},
                                    {'x': [2018], 'y': [yData3[1]], 'type': 'bar', 'name': 'Away Wins'}
                                ],
                                'layout': {
                                    'title' : 'Bar graph showing distribution',
                                    'plot_bgcolor': colors['background'],
                                    'paper_bgcolor': colors['background'],
                                    'font': {
                                        'color': colors['text']
                                    }
                                }
                            }
                            )], style={'width':'100%','display':'inline-block', 'font-family':'Georgia'}),

            html.Div([

                html.Iframe(src= "//plot.ly/~hamiri/9.embed", style={'width': '100%', 'height':'650px', 'border':'none'})# , style="border:none")
                ])
            ])

@app.callback(
     Output("my-graph", "figure"),
     [Input("season", "value")]
 )


def update_graph(selected):
    return {
        "data": [go.Pie(labels=dff["Team"].unique().tolist(), values=dff[dff["Season"] == selected]["W"].tolist(),
                        marker={'colors': ['#EF963B', '#C93277', '#349600', '#EF533B', '#57D4F1']}, textinfo='label')],
       "layout": go.Layout(title="Win Distribution by Season", margin={"l": 300, "r": 300, },
                            legend={"x": 1, "y": 0.7})}


    
    
application = app.server

if __name__ == '__main__':
    application.run(debug=True, port=8080)