import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import pdist, squareform
import networkx as nx

DATA_PATH = "data/Sample_Categorized_Data.csv"

def load_data():
    df = pd.read_csv(DATA_PATH)
    return df

def compute_similarity(df):
    # Pivot to get sample x substance matrix
    matrix = df.pivot_table(
        index='Sample number', 
        columns='Substance', 
        values='Relative area (%)',
        fill_value=0
    )

    # Cosine similarity
    cos_sim = pd.DataFrame(cosine_similarity(matrix), index=matrix.index, columns=matrix.index)

    # Euclidean distance → similarity
    eu_dist = pd.DataFrame(squareform(pdist(matrix, metric='euclidean')), index=matrix.index, columns=matrix.index)
    eu_sim = 1 / (1 + eu_dist)  # normalize

    # Jaccard similarity (binary)
    binary_matrix = (matrix > 0).astype(int)
    intersection = binary_matrix.dot(binary_matrix.T)
    union = binary_matrix.sum(axis=1).values.reshape(-1,1) + binary_matrix.sum(axis=1) - intersection
    jaccard_sim = intersection / union
    jaccard_sim = pd.DataFrame(jaccard_sim, index=matrix.index, columns=matrix.index)

    return cos_sim, eu_sim, jaccard_sim

def joint_similarity(cos, eu, jaccard, w_cos=0.33, w_eu=0.33, w_jac=0.34):
    return w_cos*cos + w_eu*eu + w_jac*jaccard

def build_network(sim_df, threshold=0.5):
    G = nx.Graph()
    for i in sim_df.index:
        G.add_node(i)
    for i in sim_df.index:
        for j in sim_df.columns:
            if i != j and sim_df.loc[i,j] >= threshold:
                G.add_edge(i, j, weight=sim_df.loc[i,j])
    return G
