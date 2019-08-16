import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from pylab import *

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

migration_df = pd.read_excel('C:/Users/mowm/Desktop/d3_plotly_testing/data/data.xlsx', 'data_coded2')

provinces = ['Newfoundland and Labrador', 'Prince Edward Island', 'Nova Scotia',
             'New Brunswick', 'Quebec', 'Ontario', 'Manitoba', 'Saskatchewan',
             'Alberta', 'British Columbia']
             
cmap = cm.get_cmap('tab20', 20)    # PiYG
colors = []
for i in range(cmap.N):
    rgb = cmap(i)[:3] # will return rgba, we take only first 3 so we get rgb
    colors.append(matplotlib.colors.rgb2hex(rgb))
    
node_colors = colors[::2]
link_colors = colors[1::2]

app.layout = html.Div([
    html.Div('Choose province of origination'),
    html.Div([
        dcc.Dropdown(
            id='select-province',
            options=[{'label': provinces[i], 'value': i} for i in range(len(provinces))],
            value=provinces.index('Ontario')
        )]),
    dcc.Graph(id='migration-sankey')
    ])
    
@app.callback(
    Output('migration-sankey', 'figure'),
    [Input('select-province', 'value')])
def update_graph(selected_province):
    df_province = migration_df[migration_df['Source']==selected_province]

    return {
            'data': [go.Sankey(
                orientation = "h",
                node = dict(
                    pad = 15,
                    thickness = 20,
                    line = dict(color = "black", width = 0.5),
                    label = provinces,
                    color = node_colors
                ),
                link = dict(
                    source = df_province['Source'].dropna(axis=0, how='any'),
                    target = df_province['Target'].dropna(axis=0, how='any'),
                    value = df_province['Value'].dropna(axis=0, how='any')
                ))],
            'layout': go.Layout(
                title='Interprovincial Migration',
                height=700,  # px
            )
        }

if __name__ == '__main__':
    app.run_server(debug=True)
