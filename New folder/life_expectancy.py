from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
app= Dash()
data=pd.read_csv('Python-Interactive-Dashboards-with-Plotly-Dash-main/life_expectancy.csv')

yearMin= data['year'].min()
yearMax= data['year'].max()

app.layout =  html.Div([
    dbc.Col([
        dbc.Row([
            dbc.Col(
                html.H1('Life Expectancy Dashboard', 
                        style={'color': 'white','textAlign': 'left'})
                ),
            dbc.Col(
                html.A('Data Source', 
                       href='https://example.com', 
                       target='_blank', 
                       style={'color': 'white'}),
                style={'textAlign': 'right'}
                )], 
            style={'backgroundColor': 'blue'}),
        dbc.Row([
            html.H4('Life expectancy by Country and Year', style={'color':'white', 'textAlign':'center'}),
            dcc.RangeSlider(
                id='year-slider',
                min=yearMin,
                max=yearMax,
                value=[yearMin, yearMax],
                marks={i: str(i) for i in range(yearMin, yearMax+1, 10)})],
            style={'backgroundColor': 'darkblue'}),
        dbc.Row(
            dcc.Dropdown(
                id='country-dropdown',
                options=data['country'].unique(),
                multi=True, style={'margin':'10px 0px 10px 0px'})),
        dbc.Row([
            html.Button(id='submit-button', n_clicks=0, children='Submit')
        ]),
        dbc.Row([
            dcc.Graph(id='graph')
        ])
    ])
])
@app.callback(
    Output('graph', 'figure'),
    Input('submit-button', 'n_clicks'),
    State('year-slider', 'value'),
    State('country-dropdown', 'value')
)
def update_figure(buttonclick, selected_years, selected_countries):
    if not selected_countries:
        return px.line(title='Please select at least one country')
    else:
        filtered_expctancy= data[data['country'].isin(selected_countries)]
        filtered_expctancy_year= filtered_expctancy[(filtered_expctancy['year']>= selected_years[0])& (filtered_expctancy['year']<=selected_years[1])]
    line_fig = px.line(
        filtered_expctancy_year,
        x='year',
        y='life expectancy',
        title='Life Expectancy',
        color='country')    
    return line_fig
    



if __name__== '__main__':
    app.run(debug=True)