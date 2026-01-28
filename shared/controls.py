# shared/controls.py
from dash import html, dcc

def weight_input_block(label, input_id, slider_id, default_value=0):
    """
    Reusable weight + slider block for similarity weights or thresholds.
    """
    return html.Div([
        html.Label(f"{label} (%)", style={'fontSize': '16px', 'fontWeight': 'bold', 'color': '#000'}),
        dcc.Input(
            id=input_id,
            type='number',
            value=default_value,
            min=0,
            max=100,
            step=1,
            style={'width':'120px', 'height':'35px', 'fontSize':'16px', 'textAlign':'center', 'marginBottom':'10px'}
        ),
        dcc.Slider(
            id=slider_id,
            min=0,
            max=100,
            step=1,
            value=default_value,
            tooltip={"placement": "bottom", "always_visible": True},
            marks={i: str(i) for i in range(0, 101, 20)}
        )
    ], style={'padding':'15px', 'margin':'10px', 'backgroundColor':'#f8f9fa', 'borderRadius':'8px'})

def chemical_filter_dropdown(dropdown_id, substances):
    """
    Multi-select dropdown for chemical substances filtering.
    """
    options = [{'label': s, 'value': s} for s in substances]
    return html.Div([
        html.H3("Filter by Chemical Components", style={'color': '#000', 'marginBottom': '15px'}),
        dcc.Dropdown(
            id=dropdown_id,
            options=[{'label': 'All', 'value': 'All'}] + options,
            value=['All'],
            multi=True,
            clearable=True,
            style={'fontSize': '16px'},
            placeholder="Select chemical components..."
        )
    ], style={'padding': '20px', 'marginBottom': '20px', 'backgroundColor': '#f8f9fa', 'borderRadius': '8px'})
