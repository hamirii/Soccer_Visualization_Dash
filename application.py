import _plotly_future_
from _plotly_future_ import v4_subplots
import dash
import dash_html_components as html
from winRecords import winRecords
import pandas as pd
import dash_core_components as dcc
import plotly
from dash.dependencies import Input, Output, State
import numpy as np
import dash_table as dt
import plotly.graph_objs as go
from plotly.subplots import make_subplots

from winRecords import winRecords
from winRecords import binaryFTR

tabdata = pd.read_csv("serieA/serieA_season-1819.csv")
resD = binaryFTR(pd.read_csv("serieA/serieA_season-1819.csv"), 'FTR')
yData1 = (winRecords(pd.read_csv("serieA/serieA_season-1617.csv"), 'SerieA_16_17', 'FTR'))
yData2 = (winRecords(pd.read_csv("serieA/serieA_season-1718.csv"), 'SerieA_17_18', 'FTR'))
yData3 = (winRecords(pd.read_csv("serieA/serieA_season-1819.csv"), 'SerieA_18_19', 'FTR'))
#xData = np.arange(len(yData[0]))
seasonsLabels = ['2016/17', '2017/18', '2018/19']
pieData17 = [yData2[0], yData2[1], yData2[2]]
pieData18 = [yData3[0], yData3[1], yData3[2]]
catLabels = ['Home wins', 'Away wins', 'Draws']

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_ebola.csv')
df = df.dropna(axis=0)
dff = pd.read_csv('serieA/saa.csv')


app = dash.Dash(__name__)

app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

colors = {
    'background': '#FFFFFF',
    'text': '#000000'
}
app.layout = html.Div([

    html.Div(

        [
            html.H1(
            children='Win Distributions in Serie A by year',
            style={
                'textAlign': 'center',
                'color': colors['text'],
                'font-family': 'Gill Sans'
            }
        ),
            html.Div([
                dcc.Tabs(id="tabs", value='stab-1', children=[
                    dcc.Tab(id = 'tab_1',label='2017/18', value='tab-1'),
                    dcc.Tab(id = 'tab_2',label='2018/19', value='tab-2'),
                ])
                ]),
            html.Div(id='tabs-content')
        ]),

    #html.Div([

        #html.Iframe(src= "https://chart-studio.plot.ly/~hamiri/6.embed", style={'width': '100%', 'height':'650px', 'border':'none'})# , style="border:none")

        #dt.DataTable(

         #   id='table',
          #  columns=[{"name": i, "id": i} for i in tabdata.columns],
           # data=tabdata.to_dict('records'),
        #)


    #]),

    html.Div([

        html.Div([html.H1("Win distribution by Season")], style={"textAlign": "center"}),
            dcc.Graph(id="my-graph"),
            html.Div([dcc.Slider(id='season', min=1, max=4, value=3,
                                marks={1: "2015/16", 2: "2016/17", 3: "2017/18", 4: "2018/19"})],
                    style={'textAlign': "center", "margin": "30px", "padding": "10px", "width": "65%", "margin-left": "auto",
                            "margin-right": "auto"}),
        ], className="container")
    

    #html.Div([
     #   html.Iframe(width='500', height='500', src='https://chart-studio.plot.ly/~hamiri/6.embed')
    #])
])


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
                            )], style={'width':'100%','display':'inline-block', 'font-family':'Georgia'})
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