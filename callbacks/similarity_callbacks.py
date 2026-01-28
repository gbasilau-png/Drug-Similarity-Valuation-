# callbacks/similarity_callbacks.py
from dash import Input, Output, State
import pandas as pd
import plotly.graph_objects as go
from shared.utils import validate_weights, create_enhanced_network
import dash

def register_similarity_callbacks(app, df_jac, df_euc, df_cos, df_substance):
    """
    Register all similarity module callbacks
    df_jac, df_euc, df_cos: DataFrames for Jaccard, Euclidean, Cosine
    df_substance: DataFrame of common substances per pair
    """

    # -------------------------------
    # Sync sliders <-> numeric inputs
    # -------------------------------
    @app.callback(
        [Output('w-jaccard','value'), Output('w-euclidean','value'), Output('w-cosine','value'), Output('threshold','value')],
        [Input('slider-jaccard','value'), Input('slider-euclidean','value'), Input('slider-cosine','value'), Input('slider-threshold','value')]
    )
    def sync_slider_to_input(sj,se,sc,st):
        return sj,se,sc,st

    @app.callback(
        [Output('slider-jaccard','value'), Output('slider-euclidean','value'), Output('slider-cosine','value'), Output('slider-threshold','value')],
        [Input('w-jaccard','value'), Input('w-euclidean','value'), Input('w-cosine','value'), Input('threshold','value')]
    )
    def sync_input_to_slider(wj,we,wc,th):
        return wj,we,wc,th

    # -------------------------------
    # Update network and table live
    # -------------------------------
    @app.callback(
        [Output('network-graph','figure'), Output('edge-table','data'), Output('joint-similarity-display','children')],
        [Input('w-jaccard','value'), Input('w-euclidean','value'), Input('w-cosine','value'), Input('threshold','value'), Input('chemical-dropdown','value')]
    )
    def update_network(w_j, w_e, w_c, threshold, selected_substances):
        try:
            # Validate weights
            validate_weights(w_j,w_e,w_c,threshold)

            # Normalize weights
            total = (w_j or 0) + (w_e or 0) + (w_c or 0)
            w_j_norm = (w_j or 0)/total if total else 0
            w_e_norm = (w_e or 0)/total if total else 0
            w_c_norm = (w_c or 0)/total if total else 0

            # Merge tables live
            df_merged = df_jac.merge(df_euc,on=['Sample_1','Sample_2']).merge(df_cos,on=['Sample_1','Sample_2'])

            # Merge substance info
            if df_substance is not None and not df_substance.empty:
                df_substance_agg = df_substance.groupby(['Sample_1','Sample_2'])['Common_Substance']\
                    .apply(lambda x:', '.join(sorted(set(x.dropna())))).reset_index().rename(columns={'Common_Substance':'Key_Substances'})
                df_merged = df_merged.merge(df_substance_agg,on=['Sample_1','Sample_2'],how='left')
            else:
                df_merged['Key_Substances']=''

            # Filter chemical
            if selected_substances and 'All' not in selected_substances:
                df_merged = df_merged[df_merged['Key_Substances'].apply(
                    lambda x: any(sub in str(x).split(', ') for sub in selected_substances)
                )]

            # Geometric mean for joint similarity
            df_merged['Joint_Similarity'] = (df_merged['Jaccard']*df_merged['Euclidean']*df_merged['Cosine'])**(1/3)

            # Threshold
            threshold_norm = (threshold or 0)/100
            df_edges = df_merged[df_merged['Joint_Similarity'] >= threshold_norm].copy()
            df_edges = df_edges.sort_values('Joint_Similarity',ascending=False).drop_duplicates(['Sample_1','Sample_2'])

            # Network figure
            fig = create_enhanced_network(df_edges) if not df_edges.empty else go.Figure()

            # Table data
            table_data = df_edges[['Sample_1','Sample_2','Joint_Similarity','Key_Substances']].to_dict('records')

            return fig, table_data, f"Showing {len(df_edges)} sample pairs above threshold."

        except Exception as e:
            return go.Figure(), [], f"❌ Error: {str(e)}"
