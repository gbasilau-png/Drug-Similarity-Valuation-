# modules/weak_profile.py
from dash import html, dcc, dash_table
import pandas as pd
import os

# Layout function
def layout():
    return html.Div([
        html.H1("Weak Profile Detection", style={'textAlign':'center','marginBottom':'30px'}),
        html.P("This module identifies weak drug profiles based on unknowns, low actives, and precursors."),
        html.Div(id='weak-profile-output')
    ])
