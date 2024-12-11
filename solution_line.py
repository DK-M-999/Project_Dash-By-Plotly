import pandas as pd
import plotly.express as px  # (version 4.7.0)

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)
df = pd.read_csv("intro_bees.csv")

# Group by relevant columns and compute the average 'Pct of Colonies Impacted'
df = df.groupby(['State', 'ANSI', 'Affected by', 'Year', 'state_code'])[['Pct of Colonies Impacted']].mean()
df.reset_index(inplace=True)
print(df[:5])

# List of bee killers for the dropdown options
bee_killers = ["Disease", "Other", "Pesticides", "Pests_excl_Varroa", "Unknown", "Varroa_mites"]

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Web Application Dashboards with Dash", style={'text-align': 'center'}),

    # Dropdown menu for selecting the bee killer type
    dcc.Dropdown(id="slct_impact",
                 options=[{"label": x, "value": x} for x in bee_killers],
                 value="Pesticides",  # default value
                 multi=False,  # allow only single selection
                 style={'width': "40%"}
                 ),

    # Display the selected value from the dropdown
    html.Div(id='output_container', children=[]),
    html.Br(),

    # Graph to display the line plot
    dcc.Graph(id='my_bee_map', figure={})

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_bee_map', component_property='figure')],
    [Input(component_id='slct_impact', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    # Container text for the chosen option
    container = "The bee-killer chosen by user was: {}".format(option_slctd)

    # Filter the dataframe based on the selected bee killer
    dff = df.copy()
    dff = dff[dff["Affected by"] == option_slctd]

    # Filter for specific states: Idaho, New York, and New Mexico
    dff = dff[(dff["State"] == "Idaho") | (dff["State"] == "New York") | (dff["State"] == "New Mexico")]

    # Create a line plot
    fig = px.line(
        data_frame=dff,
        x='Year',
        y='Pct of Colonies Impacted',
        color='State',  # Color by State
        template='plotly_dark',  # Set plotly_dark template for the graph
        title="Impact of Bee-Killers on Colonies in Selected States"  # Add title for clarity
    )

    # Return the container text and the figure for the plot
    return container, fig


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
