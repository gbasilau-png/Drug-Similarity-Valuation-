# app.py
import os
import dash
from dash import html, dcc

# ---- Load your modules ----
from shared.controls import create_controls  # weight sliders, threshold, chemical filters
from modules.similarity import similarity_layout  # similarity network layout
from modules.weak_profile import weak_profile_layout  # weak profile table layout
from callbacks.similarity_callbacks import register_similarity_callbacks
from callbacks.weak_profile_callbacks import register_weak_profile_callbacks

# ---- Initialize Dash app ----
app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = "Chemical Similarity Dashboard"

# ---- Layout ----
app.layout = html.Div([
    html.H1("Chemical Similarity Dashboard", style={"textAlign": "center"}),
    html.Hr(),

    # Shared controls (weights, threshold, chemical filters)
    create_controls(),

    html.Hr(),

    # Tabs for different modules
    dcc.Tabs(id="tabs", value="tab-similarity", children=[
        dcc.Tab(label="Similarity Analysis", value="tab-similarity"),
        dcc.Tab(label="Weak Profile Detection", value="tab-weak-profile"),
        dcc.Tab(label="Cluster Analysis", value="tab-cluster"),
        dcc.Tab(label="Trend Analysis", value="tab-trend"),
        dcc.Tab(label="Anomaly Detection", value="tab-anomaly"),
    ]),
    html.Div(id="tabs-content")  # content is updated dynamically
])

# ---- Tab content callback ----
@app.callback(
    dash.dependencies.Output("tabs-content", "children"),
    [dash.dependencies.Input("tabs", "value")]
)
def render_tab_content(tab):
    if tab == "tab-similarity":
        return similarity_layout
    elif tab == "tab-weak-profile":
        return weak_profile_layout
    else:
        return html.Div("Coming soon...")

# ---- Register callbacks ----
register_similarity_callbacks(app)
register_weak_profile_callbacks(app)

# ---- Expose server for Gunicorn ----
server = app.server

# ---- Run locally (dev) ----
if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8050)))
