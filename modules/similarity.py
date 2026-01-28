# modules/similarity.py
from dash import html
from shared.controls import weight_input_block, chemical_filter_dropdown

similarity_layout = html.Div(
    [
        html.H3("Similarity Network"),

        weight_input_block(),
        chemical_filter_dropdown(),

        html.Div(
            id="similarity-output",
            children="Network visualization will appear here.",
            style={"marginTop": "20px"},
        ),

        html.Button("Save Results", id="save-similarity", n_clicks=0),
    ]
)
