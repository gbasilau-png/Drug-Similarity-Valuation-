import dash
from dash import html, dcc, Output, Input, State
import plotly.graph_objects as go
import networkx as nx
import pandas as pd

from shared.utils import load_data, compute_similarity, joint_similarity, build_network

# Load data
df_samples = load_data()
cos_sim, eu_sim, jaccard_sim = compute_similarity(df_samples)

# Dash app
app = dash.Dash(__name__)
server = app.server  # for Gunicorn

app.layout = html.Div([
    html.H1("Chemical Sample Similarity Dashboard"),
    
    html.Div([
        html.Label("Cosine Weight"),
        dcc.Slider(id='w_cos', min=0, max=1, step=0.05, value=0.33),
        html.Label("Euclidean Weight"),
        dcc.Slider(id='w_eu', min=0, max=1, step=0.05, value=0.33),
        html.Label("Jaccard Weight"),
        dcc.Slider(id='w_jac', min=0, max=1, step=0.05, value=0.34),
        html.Label("Similarity Threshold"),
        dcc.Slider(id='threshold', min=0, max=1, step=0.05, value=0.5),
        html.Button("Save Joint Similarity CSV", id="save-btn"),
        html.Div(id="save-status")
    ], style={'width':'30%', 'display':'inline-block', 'verticalAlign':'top'}),
    
    html.Div([
        dcc.Graph(id='network-graph')
    ], style={'width':'68%', 'display':'inline-block', 'paddingLeft':20})
])

# Callback for updating network
@app.callback(
    Output('network-graph', 'figure'),
    Input('w_cos', 'value'),
    Input('w_eu', 'value'),
    Input('w_jac', 'value'),
    Input('threshold', 'value')
)
def update_network(w_cos, w_eu, w_jac, threshold):
    sim_df = joint_similarity(cos_sim, eu_sim, jaccard_sim, w_cos, w_eu, w_jac)
    G = build_network(sim_df, threshold)
    
    pos = nx.spring_layout(G, seed=42)
    edge_x, edge_y = [], []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color='#888'),
        hoverinfo='none',
        mode='lines'
    )

    node_x, node_y, node_text = [], [], []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=node_text,
        textposition="bottom center",
        hoverinfo='text',
        marker=dict(size=15, color='skyblue')
    )

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20,l=5,r=5,t=40)
                    ))
    return fig

# Callback for saving CSV
@app.callback(
    Output('save-status', 'children'),
    Input('save-btn', 'n_clicks'),
    State('w_cos', 'value'),
    State('w_eu', 'value'),
    State('w_jac', 'value')
)
def save_csv(n_clicks, w_cos, w_eu, w_jac):
    if n_clicks:
        sim_df = joint_similarity(cos_sim, eu_sim, jaccard_sim, w_cos, w_eu, w_jac)
        sim_df.to_csv("data/Joint_Similarity.csv")
        return f"Joint_Similarity.csv saved!"
    return ""

if __name__ == '__main__':
    app.run_server(debug=True)
