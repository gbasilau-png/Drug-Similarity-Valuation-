# shared/utils.py
import os
import networkx as nx
import plotly.graph_objects as go

# -------------------------------
# Environment Detection
# -------------------------------
def is_docker():
    """Check if running inside Docker."""
    return os.path.exists('/.dockerenv')

def get_bind_address():
    """Return bind address depending on environment."""
    return '0.0.0.0' if is_docker() else '127.0.0.1'

# -------------------------------
# Weight validation
# -------------------------------
def validate_weights(w_j, w_e, w_c, threshold):
    """Validate that weights and threshold are within 0-100."""
    weights = [w_j or 0, w_e or 0, w_c or 0]
    threshold = threshold or 0
    if any(w < 0 or w > 100 for w in weights + [threshold]):
        raise ValueError("Weights and threshold must be between 0-100")
    return weights

# -------------------------------
# Network Visualization
# -------------------------------
def create_enhanced_network(df_edges):
    """
    Build a Plotly figure from a DataFrame of edges with 'Sample_1', 'Sample_2', 'weight'.
    """
    G = nx.Graph()
    for _, row in df_edges.iterrows():
        G.add_edge(row['Sample_1'], row['Sample_2'], weight=row.get('Joint_Similarity', 0))

    pos = nx.spring_layout(G, seed=42, k=1, iterations=50)

    edge_traces = []
    for u, v in G.edges():
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        weight = G[u][v]['weight']
        color_intensity = max(0.3, weight)
        color = f'rgba(30, 136, 229, {color_intensity})'

        edge_traces.append(
            go.Scatter(
                x=[x0, x1, None],
                y=[y0, y1, None],
                line=dict(width=2 + weight*5, color=color),
                hoverinfo='text',
                text=f"{u}-{v}: {weight:.3f}",
                mode='lines',
                showlegend=False
            )
        )

    node_x, node_y, node_text, node_hover = [], [], [], []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)
        neighbors = list(G.neighbors(node))
        node_hover.append(f"Sample: {node}<br>Connections: {len(neighbors)}")

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=node_text,
        hovertext=node_hover,
        hoverinfo='text',
        textposition='middle center',
        marker=dict(size=20, color='lightblue', line=dict(width=2, color='darkblue')),
        showlegend=False
    )

    fig = go.Figure()
    for trace in edge_traces:
        fig.add_trace(trace)
    fig.add_trace(node_trace)

    fig.update_layout(
        title="Weighted Similarity Network",
        showlegend=False,
        hovermode='closest',
        margin=dict(b=20, l=5, r=5, t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=700,
        plot_bgcolor='white'
    )
    return fig
