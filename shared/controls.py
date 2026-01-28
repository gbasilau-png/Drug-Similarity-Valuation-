# shared/controls.py
from dash import html, dcc

def create_controls():
    """Return shared controls: weights, threshold, chemical filters"""
    return html.Div([
        html.H4("Weights & Filters"),
        html.Div([
            html.Label("Jaccard Weight (%)"),
            dcc.Slider(id="weight-jaccard", min=0, max=100, step=1, value=33),
            html.Label("Euclidean Weight (%)"),
            dcc.Slider(id="weight-euclidean", min=0, max=100, step=1, value=33),
            html.Label("Cosine Weight (%)"),
            dcc.Slider(id="weight-cosine", min=0, max=100, step=1, value=34),
        ], style={"margin-bottom": "20px"}),

        html.Label("Similarity Threshold (%)"),
        dcc.Slider(id="similarity-threshold", min=0, max=100, step=1, value=50),

        html.Label("Filter by Chemical Components"),
        dcc.Dropdown(id="chemical-filter", options=[], multi=True, placeholder="Select chemicals..."),
        html.Hr()
    ])
