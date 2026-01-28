# shared/controls.py
from dash import html, dcc


def weight_input_block():
    return html.Div(
        [
            html.H4("Similarity Weights (%)"),

            html.Label("Jaccard"),
            dcc.Slider(
                id="weight-jaccard",
                min=0, max=100, step=1, value=33,
                tooltip={"placement": "bottom"}
            ),

            html.Label("Euclidean"),
            dcc.Slider(
                id="weight-euclidean",
                min=0, max=100, step=1, value=33,
                tooltip={"placement": "bottom"}
            ),

            html.Label("Cosine"),
            dcc.Slider(
                id="weight-cosine",
                min=0, max=100, step=1, value=34,
                tooltip={"placement": "bottom"}
            ),
        ],
        style={"marginBottom": "25px"},
    )


def chemical_filter_dropdown():
    return html.Div(
        [
            html.Label("Filter by Chemical Components"),
            dcc.Dropdown(
                id="chemical-filter",
                options=[],
                multi=True,
                placeholder="Select chemicals...",
            ),
        ],
        style={"marginBottom": "25px"},
    )
