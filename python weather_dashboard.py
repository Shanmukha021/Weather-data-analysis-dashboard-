import os
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

file_path = "FORECAST -1.csv"
if not os.path.exists(file_path):
    raise FileNotFoundError(f"File not found: {file_path}")

data = pd.read_csv(file_path)
app = Dash(__name__)

def plot_figures(df):
    return [
        px.area(df, x='wind_degree', y='temperature_celsius', title='Temperature vs Wind Degree'),
        px.scatter(df, x='wind_mph', y='temperature_celsius', color='wind_degree', size='wind_kph'),
        px.histogram(df, x='wind_mph', nbins=15, title='Wind Speed Distribution'),
        px.bar(df.groupby('wind_degree', as_index=False)['temperature_celsius'].mean(), x='wind_degree', y='temperature_celsius'),
        px.box(df, x='wind_degree', y='wind_mph'),
        px.violin(df, x='wind_degree', y='temperature_celsius', box=True)
    ]

fig_area, fig_scatter, fig_histogram, fig_bar, fig_box, fig_violin = plot_figures(data)

app.layout = html.Div([
    html.H1("Weather Data Dashboard", style={'text-align': 'center'}),
    html.Div([
        html.Label("Wind Degree (°):"), dcc.Input(id='wind-degree-input', type='number', value=0, step=1),
        html.Label("Temperature (°C):"), dcc.Input(id='temperature-input', type='number', value=0, step=1)
    ], style={'text-align': 'center'}),
    html.Div([
        dcc.Graph(id='area-chart', figure=fig_area),
        dcc.Graph(id='scatter-plot', figure=fig_scatter)
    ]),
    html.Div([
        dcc.Graph(id='histogram', figure=fig_histogram),
        dcc.Graph(id='bar-chart', figure=fig_bar)
    ]),
    html.Div([
        dcc.Graph(id='box-plot', figure=fig_box),
        dcc.Graph(id='violin-plot', figure=fig_violin)
    ])
])

@app.callback(
    [Output('area-chart', 'figure'), Output('scatter-plot', 'figure'),
     Output('histogram', 'figure'), Output('bar-chart', 'figure'),
     Output('box-plot', 'figure'), Output('violin-plot', 'figure')],
    [Input('wind-degree-input', 'value'), Input('temperature-input', 'value')]
)
def update_graphs(wind_degree, temperature):
    filtered_data = data[(data['wind_degree'] >= wind_degree) & (data['temperature_celsius'] >= temperature)]
    return plot_figures(filtered_data)

if __name__ == '__main__':
    app.run_server(debug=True)
