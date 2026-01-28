# modules/similarity.py
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from shared.controls import weight_input_block, chemical_filter_dropdown
from shared.utils import validate_weights, create_enhanced_network

# -------------------------------
# Layout function
# -------------------------------
def layout(substances=[]):
    return html.Div([
        html.H1("Joint Weighted Similarity Analysis", style={'textAlign': 'center', 'marginBottom': '30px'}),
        
        # Weights + Threshold
        html.Div([
            html.Div([
                weight_input_block("Jaccard Weight", "w-jaccard", "slider-jaccard", 35),
                weight_input_block("Euclidean Weight", "w-euclidean", "slider-euclidean", 30),
                weight_input_block("Cosine Weight", "w-cosine", "slider-cosine", 35),
            ], style={'display': 'flex', 'justifyContent': 'space-between', 'flexWrap': 'wrap'}),
            
            weight_input_block("Similarity Threshold", "threshold", "slider-threshold", 80)
        ], style={'backgroundColor': '#ffffff', 'padding': '20px', 'borderRadius': '10px', 'marginBottom': '20px', 'border': '1px solid #ddd'}),
        
        # Chemical filter
        chemical_filter_dropdown('chemical-dropdown', substances),
        
        # Info display
        html.Div(id='joint-similarity-display', style={
            'border': '2px solid #007bff', 
            'padding': '15px', 
            'margin': '10px', 
            'backgroundColor': '#e7f3ff', 
            'color': '#000', 
            'fontSize': '16px',
            'fontWeight': 'bold',
            'borderRadius':'8px'
        }),
        
        # Save buttons
        html.Div([
            html.Button("💾 Save Network Diagram as PNG", id='save-diagram-btn', n_clicks=0,
                        style={'margin':'10px','padding':'10px 20px','backgroundColor':'#4CAF50','color':'white'}),
            html.Button("📊 Save Table as CSV", id='save-table-btn', n_clicks=0,
                        style={'margin':'10px','padding':'10px 20px','backgroundColor':'#2196F3','color':'white'}),
            html.Button("📋 Save Table as Excel", id='save-excel-btn', n_clicks=0,
                        style={'margin':'10px','padding':'10px 20px','backgroundColor':'#FF9800','color':'white'}),
        ], style={'display':'flex','justifyContent':'center','flexWrap':'wrap','padding':'20px'}),
        
        # Graph
        html.Div([dcc.Graph(id='network-graph')], style={'width':'100%','marginTop':'20px','marginBottom':'30px'}),
        
        # Table
        html.Div([
            html.H4("Sample Pairs Above Threshold", style={'textAlign':'center','marginBottom':'15px'}),
            dash_table.DataTable(
                id='edge-table',
                columns=[
                    {'name':'Sample 1','id':'Sample_1','type':'text'},
                    {'name':'Sample 2','id':'Sample_2','type':'text'},
                    {'name':'Joint Similarity','id':'Joint_Similarity','type':'numeric','format':{'specifier':'.3f'}},
                    {'name':'Common Substances','id':'Key_Substances','type':'text'}
                ],
                style_table={'overflowX':'auto','maxHeight':'600px','overflowY':'auto'},
                style_cell={'textAlign':'center','fontSize':'14px','padding':'10px','minWidth':'100px'},
                style_header={'backgroundColor':'rgb(230,230,230)','fontWeight':'bold','fontSize':'14px'},
                style_data_conditional=[{'if':{'row_index':'odd'},'backgroundColor':'rgb(248,248,248)'}],
                sort_action='native',
                filter_action='native',
                filter_options={'case':'insensitive'},
                page_action='native',
                page_size=10,
                row_selectable='single'
            )
        ], style={'width':'100%','marginTop':'10px'}),
        
        # Hidden downloads
        dcc.Download(id="download-csv"),
        dcc.Download(id="download-excel"),
        dcc.Download(id="download-png"),
    ])

# -------------------------------
# Callbacks registration
# -------------------------------
def register_callbacks(app, df_jac, df_euc, df_cos, df_substance):
    """
    All callbacks related to similarity analysis
    df_jac, df_euc, df_cos: DataFrames for Jaccard, Euclidean, Cosine
    df_substance: DataFrame of common substances per pair
    """

    # Sync sliders <-> inputs
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

    # Update network and table
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
            if total==0:
                w_j_norm = w_e_norm = w_c_norm = 0
            else:
                w_j_norm = (w_j or 0)/total
                w_e_norm = (w_e or 0)/total
                w_c_norm = (w_c or 0)/total

            # Merge tables on-the-fly
            df_merged = df_jac.merge(df_euc,on=['Sample_1','Sample_2']).merge(df_cos,on=['Sample_1','Sample_2'])
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

            # -------------------------------
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
