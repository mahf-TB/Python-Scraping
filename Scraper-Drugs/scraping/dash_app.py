import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
from sklearn.cluster import KMeans
import dash_bootstrap_components as dbc
import importlib 



def data_scraper(module , nb):
    print('================================================================')
    try:
        scraper = importlib.import_module(f"scraping.{module}.main")
        entry_point = getattr(scraper, 'default')
        data =  entry_point(nb)
        return data
    except ModuleNotFoundError:
        return f"module {module} not found"
    except Exception:
        return []

def clustering_data(nb):
    
    df_reviews = data_scraper('drugs', nb)
    
    X = df_reviews[['note', 'comments']]
    kmeans = KMeans(n_clusters=5).fit(X)
    df_reviews['cluster'] = kmeans.labels_
    
    print(df_reviews)
    
    return df_reviews


def setup_dash(app, nb_data):
    
    dash_app = dash.Dash(__name__, server=app, url_base_pathname='/dash/',  external_stylesheets=[dbc.themes.BOOTSTRAP])
    
    dash_app.layout = dbc.Container(
        [
            html.H1("Clustering des Médicaments", className="text-center my-4"),
            dcc.Interval(id="interval-component", interval=60*10000, n_intervals=0),  # 60 secondes
            dcc.Graph(id='line-chart')
        ],
        fluid=True,
    )
    
    print(nb_data)
    
    @dash_app.callback(
        Output('line-chart', 'figure'),
        [Input('interval-component', 'n_intervals')]
    )
    def update_line_chart(n):
        # Clustering
        df_reviews = clustering_data(nb_data)
        fig = px.scatter(df_reviews, x='comments', y='note', color='cluster', hover_data=['drug_name'])
        return fig
    

