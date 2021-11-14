# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("Data/spacex_launch_dash.csv")
launch_sites = spacex_df['Launch Site'].unique()
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Creating a dash application
app = dash.Dash(__name__)

# Creating the app layout
app.layout = html.Div(children = [html.H1('SpaceX Launch Records Dashboard',
                                        style = {'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # Adds a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id = 'site_dropdown',
                                            options = [
                                                {'label': 'All Sites', 'value': 'ALL'},
                                                {'label': launch_sites[0], 'value': launch_sites[0]},
                                                {'label': launch_sites[1], 'value': launch_sites[1]},
                                                {'label': launch_sites[2], 'value': launch_sites[2]},
                                                {'label': launch_sites[3], 'value': launch_sites[3]},
                                            ],
                                            value = 'ALL',
                                            placeholder = "Select a Launch Site here",
                                            searchable = True
                                            ),
                                html.Br(),

                                # Adding a pie chart to show the total successful launches count for all sites
                                # If a specific launch site is selected, we show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id = 'success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                html.P("Adjust the slider to range the Payload Mass"),
                                # Adding a slider to select payload range
                                dcc.RangeSlider(
                                    id = 'payload_slider',
                                    min = 0,
                                    max = 10000,
                                    step = 1000,  
                                    marks = {
                                            0: '0 kg', 1000: '1000 kg', 2000: '2000 kg', 3000: '3000 kg', 4000: '4000 kg', 5000: '5000 kg',
                                            6000: '6000 kg', 7000: '7000 kg', 8000: '8000 kg', 9000: '9000 kg', 10000: '10000 kg' },

                                    value = [min_payload,max_payload]
                                ),

                                # Places a scatter chart showing the correlation between payload and launch success
                                html.Div(dcc.Graph(id = 'success-payload-scatter-chart')),
                                ])

# Callback function decorator to specify function input and output - pie_chart
@app.callback(Output(component_id = 'success-pie-chart', component_property = 'figure'),
              Input(component_id = 'site_dropdown', component_property = 'value'))
              
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        dtf  = spacex_df[spacex_df['class'] == 1]
        fig = px.pie(dtf, names = 'Launch Site',hole=.3,title = 'Total Success Launches By all sites')
    else:
        dtf  = spacex_df.loc[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(dtf, names = 'class',hole=.3,title = 'Total Success Launches for site '+entered_site)
    return fig
        # return the outcomes piechart for a selected site

    
# Callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
# Scatter plot display

@app.callback(
     Output(component_id = 'success-payload-scatter-chart',component_property = 'figure'),
     [Input(component_id = 'site_dropdown',component_property = 'value'),Input(component_id = "payload_slider", component_property = "value")])

def update_scattergraph(entered_site,payload_slider):
    if entered_site == 'ALL':
        low, high = payload_slider
        dtf  = spacex_df
        mask = (dtf['Payload Mass (kg)'] > low) & (dtf['Payload Mass (kg)'] < high)
        fig = px.scatter(
            dtf[mask], x = "Payload Mass (kg)", y = "class", 
            color = "Booster Version",
            size = 'Payload Mass (kg)',
            hover_data = ['Payload Mass (kg)'])
    else:
        low, high = payload_slider
        dtf  = spacex_df.loc[spacex_df['Launch Site'] == entered_site]
        mask = (dtf['Payload Mass (kg)'] > low) & (dtf['Payload Mass (kg)'] < high)
        fig = px.scatter(
            dtf[mask], x = "Payload Mass (kg)", y = "class", 
            color = "Booster Version",
            size = 'Payload Mass (kg)',
            hover_data = ['Payload Mass (kg)'])
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()