from dash import Dash, html, dcc, dash_table, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

electricity = pd.read_csv('Python-Interactive-Dashboards-with-Plotly-Dash-main/electricity.csv')

app = Dash(external_stylesheets=[dbc.themes.SOLAR])

year_min= electricity['Year'].min()
year_max= electricity['Year'].max()

app.layout = html.Div([
    html.H1('Electricity Prices by US State'),
    dcc.RangeSlider(id= 'year-slider',
                    min=year_min,
                    max=year_max,
                    value= [year_min, year_max],
                    marks= {i: str(i) for i in range(year_min, year_max+1)}
                    ),
    dcc.Graph(id='price-map'),
    html.Div(id='click-children'),
    dash_table.DataTable(id='price-info')  
])

@app.callback(
 Output('price-map', 'figure'),
 Input('year-slider', 'value')
)
def update_map_graph(selected_years):
    filtered_electricity= electricity[(electricity['Year']>= selected_years[0]) & (electricity['Year']<= selected_years[1])]
    avg_price_electricity= filtered_electricity.groupby('US_State')['Residential Price'].mean().reset_index()
    map_fix= px.choropleth(avg_price_electricity,
                       locations='US_State',
                       locationmode='USA-states',
                       color='Residential Price',
                       color_continuous_scale='greens',
                       scope='usa'
                       )
    return map_fix
    
@app.callback(
    Output('price-info', 'data'),
    Input('price-map', 'clickData'),
    Input('year-slider', 'value')
)
def update_datatable(clickData, selected_years):
    if clickData is None:
        return []
    us_state= clickData['points'][0]['location']
    filtered_state= electricity[(electricity['Year']>= selected_years[0]) & 
                                (electricity['Year']<= selected_years[1]) & 
                                (electricity['US_State']== us_state)]
    return filtered_state.to_dict('records')

if __name__ == '__main__':
    app.run(debug=True)