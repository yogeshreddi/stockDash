import pandas_datareader.data as web
import datetime as dt

import pandas as pd
import numpy as np

import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output,Input,State

import dash_auth

import plotly.graph_objs as go

USERNAME_PASSWORD_PAIRS = [['Username','Password'],['yogesh','yogesh@1234']]

nsdq = pd.read_csv('NASDAQcompanylist.csv')

sectorOptions = [{'label':'myTopStocks','value':0},
            {'label':'AllSectors','value':1}]
sectorOptions.extend([{'label':sector,'value':sector} for sector in nsdq.Sector.unique()])

app = dash.Dash()
auth = dash_auth.BasicAuth(app,USERNAME_PASSWORD_PAIRS)

app.layout = html.Div([
                  html.H1('Stock Ticker Dashboard:'),

                  html.Div([html.H3(children = 'Select sector:',
                                        style = {'paddingRight':'30px'}),
                            dcc.Dropdown(id = 'sector-name',
                                         options = sectorOptions
                                           )]),
                  html.Div([html.H3(children = 'Select stock symbols:',
                                    style = {'paddingRight':'50px'}),
                          dcc.Dropdown(id = 'stock-name',
                                       options = [{'label':row['Name'],'value':row['Symbol']} for index,row in nsdq.iterrows()],
                                       multi=True
                            )
                     ],style ={'width':'30%','float':'left'}
                ),

                html.Div([html.H3('Select start and end dates:',
                                     style = {'paddingRight':'30px'}),
                                     #style ={'width':'50%','float':'right'}),
                            dcc.DatePickerRange(
                                             id='stock-dates-range',
                                             start_date=dt.datetime(2018, 1, 1),
                                             end_date=dt.datetime.today()
                            )
                      ],
                      style={'display':'inline-block'}
                ),
                 html.Div([html.Button(id = 'submit-button',
                                       children = 'SUBMIT',
                                        n_clicks = 0)
                          ],
                          style={'display':'inline-block'}
                ),
                dcc.Graph(id = 'stock-graph')
])


@app.callback(Output('stock-name','options'),
              [Input('sector-name','value')])
def return_stock_symbols(sector_name):
    if sector_name == 0:
        options = [{'label':'myTopStocks','value':0}]
    elif sector_name == 1:
        options = [{'label':row['Name'],'value':row['Symbol']} for index,row in nsdq.iterrows()]
    else:
        df = nsdq[nsdq.Sector == sector_name]
        options = [{'label':row['Name'],'value':row['Symbol']} for index,row in df.iterrows()]
    return options

@app.callback(Output('stock-graph','figure'),
             [Input('submit-button','n_clicks')],
             [State('stock-name','value'),
              State('stock-dates-range','start_date'),
              State('stock-dates-range','end_date')])
def return_stock_graph(n_clicks,stockNames,start_date,end_date):
    if stockNames[0]==0:
        stockNames = ['TSLA','AAPL','MSFT','FB','AMZN','GOOG']
    start = dt.datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = dt.datetime.strptime(end_date[:10], '%Y-%m-%d')
    data = []
    layout = go.Layout(title = '{} closing price'.format(' '.join(stockNames)))
    for stockName in stockNames:
        df = web.DataReader(stockName,'yahoo', start, end).reset_index()
        data.append(go.Scatter(x = df.Date,
                               y = df.Close,
                               mode = 'lines',
                               name = stockName))
    #print(df.head())
    #print(df.shape)
    figure = go.Figure(data = data,
                      layout = layout)
    return(figure)


if __name__=='__main__':
    app.run_server()
