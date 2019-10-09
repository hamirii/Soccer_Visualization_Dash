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

labels = ["US", "China", "European Union", "Russian Federation", "Brazil", "India", 
          "Rest of World"]

# Create subplots: use 'domain' type for Pie subplot
fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
fig.add_trace(go.Pie(labels=labels, values=[16, 15, 12, 6, 5, 4, 42], name="GHG Emissions"),
              1, 1)
fig.add_trace(go.Pie(labels=labels, values=[27, 11, 25, 8, 1, 3, 25], name="CO2 Emissions"),
              1, 2)

# Use `hole` to create a donut-like pie chart
fig.update_traces(hole=.4, hoverinfo="label+percent+name")

fig.layout.update(
    title_text="Global Emissions 1990-2011",
    # Add annotations in the center of the donut pies.
    annotations=[dict(text='GHG', x=0.18, y=0.5, font_size=20, showarrow=False),
                 dict(text='CO2', x=0.82, y=0.5, font_size=20, showarrow=False)])
fig.show()


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

    html.Div([

        html.Iframe(src= "https://chart-studio.plot.ly/~hamiri/6.embed", style={'width': '100%', 'height':'650px', 'border':'none'})# , style="border:none")

        #dt.DataTable(

         #   id='table',
          #  columns=[{"name": i, "id": i} for i in tabdata.columns],
           # data=tabdata.to_dict('records'),
        #)


    ])

    #html.Div([
     #   html.Iframe(width='500', height='500', src='https://chart-studio.plot.ly/~hamiri/6.embed')
    #])
])

@app.callback(Output('tabs-content', 'children'),
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
    
application = app.server

if __name__ == '__main__':
    application.run(debug=True, port=8080)