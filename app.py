# app.py
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import os

# Import modules
from modules import similarity, weak_profile
from shared.controls import weight_input_block
from shared.utils import is_docker, get_bind_address
from callbacks import register_callbacks

# Initialize app
app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server

# -------------------------------
# Sidebar / Header for module navigation
# -------------------------------
sidebar = html.Div([
    html.H2("Forensic Analysis Dashboard", style={'textAlign': 'center', 'marginBottom': '30px'}),
    dcc.Tabs(id="tabs-module", value='similarity', children=[
        dcc.Tab(label='Similarity Analysis', value='similarity'),
        dcc.Tab(label='Weak Profile Detection', value='weak_profile'),
        dcc.Tab(label='Cluster Analysis', value='cluster'),   # Placeholder
        dcc.Tab(label='Trend Analysis', value='trend'),       # Placeholder
        dcc.Tab(label='Anomaly Detection', value='anomaly'),  # Placeholder
    ])
], style={'width': '20%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '20px', 'backgroundColor': '#f8f9fa'})

# -------------------------------
# Main content container
# -------------------------------
content = html.Div(id='page-content', style={'width': '75%', 'display': 'inline-block', 'padding': '20px'})

# -------------------------------
# App Layout
# -------------------------------
app.layout = html.Div([
    sidebar,
    content
])

# -------------------------------
# Page routing
# -------------------------------
@app.callback(
    Output('page-content', 'children'),
    Input('tabs-module', 'value')
)
def display_module(tab_value):
    if tab_value == 'similarity':
        return similarity.layout()
    elif tab_value == 'weak_profile':
        return weak_profile.layout()
    # Placeholder modules
    elif tab_value == 'cluster':
        return html.H3("Cluster Analysis Module Coming Soon...")
    elif tab_value == 'trend':
        return html.H3("Trend Analysis Module Coming Soon...")
    elif tab_value == 'anomaly':
        return html.H3("Anomaly Detection Module Coming Soon...")
    else:
        return html.H3("Select a module from the sidebar.")

# -------------------------------
# Register all callbacks
# -------------------------------
register_callbacks(app)

# -------------------------------
# Run server (development mode)
# -------------------------------
def main():
    print(f"🏃‍♂️ Starting app in {'Docker' if is_docker() else 'Local'} environment")
    print(f"🌐 Server will be available at: {get_bind_address()}:8050")
    if __name__ == '__main__':
        app.run_server(debug=True, host=get_bind_address(), port=8050)

if __name__ == '__main__':
    main()
