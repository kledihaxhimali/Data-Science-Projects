from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px
avocado= pd.read_csv('Python-Interactive-Dashboards-with-Plotly-Dash-main/avocado.csv')
app= Dash()

app.layout= html.Div([
    html.H1('Avocado Prices and Sales Dashboard'),
    dcc.Dropdown(id='state-dropdown', options=avocado['geography'].unique(), value='California'),
    html.Br(),
    dcc.Graph(id='avocado-graph')
])

@app.callback(
    Output('avocado-graph', 'figure'),
    Input('state-dropdown', 'value')
)
def update_graph(selected_state):
    filtered_state= avocado[avocado['geography'] == selected_state]
    line_fig = px.line(
        filtered_state,
        x='date',
        y='average_price',
        title=f'Average Avocado Prices in {selected_state}', color='type',
    )
    
    return line_fig


if __name__== '__main__':
    app.run(debug=True)