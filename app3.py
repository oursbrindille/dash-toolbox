import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import re 
import json

import pandas as pd 

dfcom = pd.read_csv("data/communes-creuse.csv",dtype=str)
dfcom = dfcom[['com','libelle','random']]
dfcom = dfcom.rename(columns={"com":"Code Insee","libelle":"Nom de la commune"})

dfetab = pd.read_csv("data/etab-creuse.csv")
dfetab2 = dfetab[['nom_etablissement','annee_scolaire','nombre_d_eleves']].pivot_table(index="annee_scolaire",columns="nom_etablissement",aggfunc="sum")
dfetab2.columns = dfetab2.columns.droplevel(0)

dflocetab = pd.read_csv("data/etabloc-creuse.csv",dtype=str)

import plotly.graph_objects as go

with open('data/testcom.json') as json_file:
    comgeojson = json.load(json_file)

fig = go.Figure(data=[go.Scattermapbox(lat=[0], lon=[0])])

fig.update_layout(
    margin={"r":0,"t":0,"l":0,"b":0},
    mapbox=go.layout.Mapbox(
        style="stamen-terrain", 
        zoom=8, 
        center_lat = 46.03351,
        center_lon = 1.84148,
        layers=[{
            'sourcetype': 'geojson',
            'source': comgeojson,
            'type': 'line',
        }]
    )
)
fig.show()


import plotly.express as px


fig2 = px.choropleth_mapbox(dfcom, geojson=comgeojson,
                           locations='Code Insee', color='random', hover_name="Nom de la commune",
                           color_continuous_scale="Viridis",
                           range_color=(0, 12),
                           mapbox_style="carto-positron",
                           zoom=8, center = {"lat": 46.03351, "lon": 1.84148},
                           opacity=0.5,
                           labels={'unemp':'unemployment rate'}
                          )
fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig2.show()


fig3 = go.Figure(go.Scattermapbox(
        lat=dflocetab.Latitude,
        lon=dflocetab.Longitude,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=9
        ),
        text=dflocetab['Dénomination principale']+" "+dflocetab["Patronyme uai"],
    ))

fig3.update_layout(
    autosize=False,
    width=900,
    height=800,
    hovermode='closest',
    mapbox=dict(
        accesstoken="pk.eyJ1Ijoic2Fib3N0aXgiLCJhIjoiY2tlcjNtOTlpMHJ5ZjJ3cDZocGU4eTRjcCJ9.ymRbs_4EvykBxJy1vBLxeA",
        bearing=0,
        center=dict(
            lat = 46.03351,
            lon = 1.84148
        ),
        pitch=0,
        zoom=8,
        style="carto-positron"
    ),
)

fig3.show()

app = dash.Dash()

app.layout = html.Div(
    style={"maxWidth":"900px", "margin":"auto","fontFamily":"medium-content-title-font, Georgia, Cambria, 'Times New Roman', Times, serif","lineHeight":"32px","letterSpacing":"-0.003em","marginTop":"2em","color":"rgba(41,41,41,1)","fontSize":"21px","textAlign":"justify"},
    children=[



        dcc.Markdown('''
            # Etude sur la Creuse
            Dans cette analyse, nous allons pouvoir visualiser plusieurs choses : 
            - Liste des communes
            - Nombre d'élèves par établissements scolaires
            - visualisation des cantons
            - visualisation des parcelles cadastrales.

            C'est parti !
            
            ## Liste des communes


        '''),


        dcc.Markdown('''
            It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).
        '''),


        dcc.Markdown('''
            Entrer un nom de commune :
        '''),
        dcc.Input(id="input",value='',type='text'),
        html.Br(),
        html.Br(),
        html.Div(id='output'),

        html.Br(),
        html.Br(),

        dcc.Markdown('''
            ## Nombre d'élèves par établissements : 
        '''),

        dcc.Markdown('''
            It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).
        '''),
        dcc.Graph(id='toto',
            figure={
                'data': [
                    {'x':dfetab[dfetab['annee_scolaire'] == '2019-2020'].nom_etablissement, 'y':dfetab[dfetab['annee_scolaire'] == '2019-2020'].nombre_d_eleves, 'type':'bar','name':'élèves'}
                ],
                'layout':  {
                    'title':'Nb d\'élèves par établissements en 2019-2020'
                }
            }),

        html.Br(),
        html.Br(),
        
        dcc.Markdown('''
            It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).
        '''),

        
        dcc.Markdown('''
            Filtrer sur un établissement :
        '''),

        dcc.Input(id="input2",value='',type='text'),
        html.Br(),
        html.Br(),
        html.Div(id='output2'),
        
        html.Br(),
        html.Br(),

        dcc.Markdown('''
            ## Délimitation des communes 
        '''),

        dcc.Markdown('''
            It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).
        '''),
        dcc.Graph(figure=fig),

        html.Br(),
        html.Br(),

        dcc.Markdown('''
            It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).
        '''),
        dcc.Graph(figure=fig2),

        html.Br(),
        html.Br(),

        dcc.Markdown('''
            It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).
        '''),
        
        dcc.Graph(figure=fig3),


        html.Br(),
        html.Br()
    ]
)


@app.callback(
    Output(component_id='output',component_property='children'),
    [Input(component_id='input',component_property='value')]
)
def update_value(input_data):
    try:
        dfcomtosend = dfcom
        dfcomtosend = dfcomtosend[dfcomtosend['Nom de la commune'].str.contains(input_data,case=False)]
        return dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in dfcomtosend.columns],
            data=dfcomtosend.head(20).to_dict('records'),
        )
    except:
        return "Problemmm"



@app.callback(
    Output(component_id='output2',component_property='children'),
    [Input(component_id='input2',component_property='value')]
)
def update_value2(input_data):
    try:
        dfetab3 = dfetab2 
        dfetab3 = dfetab3.filter(regex=re.compile(input_data, re.IGNORECASE))
        return dcc.Graph(id='tptp',
            figure={
                'data': [
                    {'x':dfetab3.index, 'y':dfetab3[i], 'type':'chart','name':i} for i in dfetab3.columns
                ],
                'layout':  {
                    'title':'Evolution du Nb d\'élèves par établissements'
                }
            })
    except:
        return "Problemmm"


if __name__ == "__main__":
    app.run_server(debug=True)
