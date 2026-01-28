# callbacks/__init__.py
from .similarity_callbacks import register_similarity_callbacks
from .weak_profile_callbacks import register_weak_profile_callbacks

def register_callbacks(app):
    """
    Register all callbacks for the Dash app.
    """
    register_similarity_callbacks(app)
    register_weak_profile_callbacks(app)
