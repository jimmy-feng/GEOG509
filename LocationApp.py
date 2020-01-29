from dash import Dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from pandas_datareader import data
import pandas as pd
import re

df = pd.read_csv("C:/Users/jfeng/OneDrive - University of Tennessee/GEOG509/Instagram/KDE/loc_all_final.csv")
df2 = df[["ArcGISAddress", "Community", "Latitude", "Longitude"]]
df = df[["ArcGISAddress", "Community", "Latitude", "Longitude"]]
df[' index'] = range(1, len(df) + 1)
df = df.rename(columns = {
                     "ArcGISAddress": "Address",
					 "Community": "Community",
                     "Latitude": "Latitude",
                     "Longitude": "Longitude"
                })
df2[' index'] = range(1, len(df2) + 1)
df2 = df2.rename(columns = {
                     "ArcGISAddress": "Address",
					 "Community": "Community",
                     "Latitude": "Latitude",
                     "Longitude": "Longitude"
                })
df = df[["Address", "Community", "Latitude", "Longitude"]]
df2 = df2[["Address", "Community", "Latitude", "Longitude"]]
filtered_df = df
filtered_df2 = df2

all_options = ['Downtown Knoxville', 'Knox County', 'Knoxville Police', 'Nourish Knoxville', 'Outdoors', 'Religious', 'Sunrise Supermarket', 'Tennessee', 'UTK', 'UTK Geography']
dictOfOptions = dict(zip(all_options, all_options))
dictOfOptions2 = [{key : value} for key, value in dictOfOptions.items()]

app = Dash()

PAGE_SIZE = 10

fig=px.scatter_mapbox(
                data_frame = df,
                lon = df['Longitude'], 
                lat = df['Latitude'],
                color = df['Community'],
                hover_name = df['Address'],
                size_max = 20,
                zoom = 1,
                )

fig.update_layout(
    title = dict(
        text = "Distribution of Communities",
        y = 0.99,
        x = 0.5,
        xanchor = 'center',
        yanchor = 'top'
    ),
    xaxis_title = "Longtiude",
    yaxis_title = "Latitude",
    legend = dict(
        font = dict(
            family = "Droid Serif"),
    ),
    mapbox_accesstoken = 'pk.eyJ1IjoiamZlbmduZ3MiLCJhIjoiY2p6Ym1iNWo4MDB1cTNicDRzcGQ2eGF1NSJ9.Ezuinvb1KJWFvQwaQj7u1A',
    mapbox = dict(
        style = 'streets',
        center = dict(
            lon = -80.8431,
            lat = 35.2271
        )
    ),
    font = dict(
        family = "Droid Serif",
        size = 18,
        color = "#7f7f7f"
    ),
    geo = dict(
        subunitcolor = 'forestgreen'
    )
)

style = dict(
    font = 'Droid Serif',
)

app.layout = html.Div(children = [
    html.Div([
        html.Div([
        html.H1(children="An Interactive Data Visualization Platform of Communities")
    ]),

        
    # Map
    html.Div([      
        html.H2(children="Map of the Extent of Communities"),]),
    
    # Input        
    html.Div([
        html.H4(children="Filter by a community"),
        dcc.Dropdown(id='dropdown', options=[{'label': k, 'value': v} for x in dictOfOptions2 for k,v in x.items()], value='Downtown Knoxville'),
    ]),    
    html.Div(
        id='map',
        children=dcc.Graph(
                figure=fig,
                style={"width": "200%", "display": "inline-block"},
            )
        , 
        className="two columns",
        ),
        
        # Table
        html.H2(children="Data Table of Georeferenced Posts by Instagram Users in a Community"),
           
        dt.DataTable(
            id='datatable-paging',
            columns=[{"name": i, "id": i} for i in filtered_df2.columns],
            page_current=0,
            page_size=PAGE_SIZE,
            page_action='custom',
            style_cell={'textAlign': 'left', 'padding':'5px', 'border': '1px solid grey'},
            style_cell_conditional=[
                {'if': {'column_id': 'index'}, 'textAlign': 'center'},
            ],
            style_header={'fontWeight':'bold', 'border': '1px solid black'},
            style_as_list_view=True,
         ),
])])

@app.callback(
    Output('datatable-paging', 'data'),
    [Input('datatable-paging', "page_current"),
     Input('datatable-paging', "page_size"),
     Input(component_id='dropdown', component_property='value')],
)
def update_table(page_current,page_size,businesstype):
    keyword = [businesstype]
    mask = df["Community"].apply(lambda x: any(item for item in keyword if item in x))
    filtered_df2 = df2[mask]
    return filtered_df2.iloc[
        page_current*page_size:(page_current+ 1)*page_size
    ].to_dict('records')

@app.callback(
    Output(component_id='map', component_property='children'),
    [Input(component_id='dropdown', component_property='value')],
)
def update_map(communitytype):
    keyword = [communitytype]
    mask = df["Community"].apply(lambda x: any(item for item in keyword if item in x))
    filtered_df = df[mask]

    newfig=px.scatter_mapbox(
               data_frame = filtered_df,
               lon = filtered_df['Longitude'], 
               lat = filtered_df['Latitude'],
               color = filtered_df['Community'],
               hover_name = filtered_df['Address'],
               size_max = 10,
               zoom = 1,
           )
    
    newfig.update_layout(
        title = dict(
        text = "Communities and their Extent on Instagram",
        y = 0.99,
        x = 0.5,
        xanchor = 'center',
        yanchor = 'top'
            ),
        xaxis_title = "Longtiude",
        yaxis_title = "Latitude",
        legend = dict(
            font = dict(
                family = "Droid Serif"),
        ),
        mapbox_accesstoken = 'pk.eyJ1IjoiamZlbmduZ3MiLCJhIjoiY2p6Ym1iNWo4MDB1cTNicDRzcGQ2eGF1NSJ9.Ezuinvb1KJWFvQwaQj7u1A',
        mapbox = dict(
            style = 'carto-positron',
            center = dict(
            lon = -80.8431,
            lat = 35.2271
        )
        ),
        font = dict(
            family = "Droid Serif",
            size = 18,
            color = "#7f7f7f"
        ),
        geo = dict(
            subunitcolor = 'forestgreen'
        )
)
    
    graph = dcc.Graph(
                figure=newfig,
                style={"width": "60%", "display": "inline-block"},
            )
    return graph

app.external_spreadsheets = 'https://codepen.io/chriddyp/pen/bWLwgP.css'

if __name__ == '__main__':
    app.run_server(debug=True)