import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

from gql import gql, Client, AIOHTTPTransport

# Select your transport with a defined url endpoint
transport = AIOHTTPTransport(url="https://countries-274616.ew.r.appspot.com/")

# Create a GraphQL client using the defined transport
client = Client(transport=transport, fetch_schema_from_transport=True)

# Provide a GraphQL query
query = gql(
    """
    query {
        Country {
          name
          population
          gini
          area
        }
    }
    """
)

# Execute the query on the transport
result = client.execute(query)
df = pd.json_normalize(result, "Country")
df.dropna()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


fig = px.scatter(df, x="area", y="gini",
                 size="population", hover_name="name",
                 log_x=True, size_max=60)

app.layout = html.Div([
     html.H1(children='Plotly Dash'),

    html.Div(children='''
        GraphQLのpythonクライアントのGQL、FWはPlotly Dashを使用
    '''),
    html.Div(children='''
        グラフはGraphQLサーバーが取得した国ごとのデータ。x軸がジニ係数、
        y軸が面積、点の大きさが人口を表しています。
    '''),
    dcc.Graph(
        id='area-vs-gini',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)