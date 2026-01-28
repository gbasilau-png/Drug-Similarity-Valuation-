# callbacks/weak_profile_callbacks.py
from dash import Input, Output
import pandas as pd

def register_weak_profile_callbacks(app, weak_summary_path, weak_samples_path):
    """
    Registers callbacks to update weak profile tables
    weak_summary_path: path to merged summary CSV
    weak_samples_path: path to weak samples CSV
    """

    @app.callback(
        Output('weak-profile-output','children'),
        Input('weak-profile-output','id')  # Dummy input to trigger callback once
    )
    def load_weak_profiles(_):
        try:
            if not os.path.exists(weak_samples_path) or not os.path.exists(weak_summary_path):
                return "⚠️ Weak profile CSVs not found."

            df_samples = pd.read_csv(weak_samples_path)
            df_summary = pd.read_csv(weak_summary_path)

            table = df_samples.to_dict('records')

            from dash import dash_table
            return dash_table.DataTable(
                columns=[{"name": i, "id": i} for i in df_samples.columns],
                data=table,
                style_table={'overflowX':'auto','maxHeight':'600px','overflowY':'auto'},
                style_cell={'textAlign':'center','padding':'8px'},
                style_header={'backgroundColor':'rgb(230,230,230)','fontWeight':'bold'},
                page_size=10,
                sort_action='native',
                filter_action='native',
                row_selectable='single'
            )
        except Exception as e:
            return f"❌ Error loading weak profiles: {str(e)}"
