import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px

def load_data():
    spacex_df = pd.read_csv("spacex_launch_dash.csv")
    return spacex_df

app = dash.Dash(__name__)

def create_layout():
    spacex_df = load_data()

    launch_sites = [{'label': 'All Sites', 'value': 'All Sites'}] + [{'label': item, 'value': item} for item in spacex_df["Launch Site"].unique()]

    layout = html.Div(
        children=[
            html.H1('SpaceX Launch Records Dashboard',
                    style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
            
            dcc.Dropdown(id='site-dropdown', options=launch_sites, value='All Sites',
                         placeholder="Select a Launch Site here", searchable=True),
            html.Br(),

            html.Div(dcc.Graph(id='success-pie-chart')),
            html.Br(),

            html.P("Payload range (Kg):"),
            dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000, 
                            value=[spacex_df['Payload Mass (kg)'].min(), spacex_df['Payload Mass (kg)'].max()],
                            marks={2500: {'label': '2500 (Kg)'}, 5000: {'label': '5000 (Kg)'}, 7500: {'label': '7500 (Kg)'}}),

            html.Div(dcc.Graph(id='success-payload-scatter-chart')),
        ]
    )
    return layout

app.layout = create_layout()

def update_graph(input_value, payload_range):
    spacex_df = load_data()

    if input_value == 'All Sites':
        filtered_df = spacex_df.copy()
    else:
        filtered_df = spacex_df[spacex_df["Launch Site"] == input_value]

    filtered_df = filtered_df[(filtered_df["Payload Mass (kg)"] >= payload_range[0]) &
                              (filtered_df["Payload Mass (kg)"] <= payload_range[1])]

    pie_chart = px.pie(filtered_df, names='class', title='Total Success Launches for ' + input_value)
    scatter_chart = px.scatter(filtered_df, y="class", x="Payload Mass (kg)", color="Booster Version Category")

    return pie_chart, scatter_chart

@app.callback([Output(component_id='success-pie-chart', component_property='figure'),
               Output(component_id='success-payload-scatter-chart', component_property='figure')],
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])
def update_charts(input_value, payload_range):
    pie_chart, scatter_chart = update_graph(input_value, payload_range)
    return pie_chart, scatter_chart

if __name__ == '__main__':
    app.run_server()
