# app.py - Main application entry point with Dark Mode and Custom Favicon

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

from components import (
    create_header,
    create_info_banner,
    create_predict_button,
    create_footer,
    create_theme_toggle,
    get_all_feature_cards
)
from callbacks import register_callbacks

# Check for imbalanced-learn
try:
    import imblearn
except ImportError:
    print("WARNING: 'imbalanced-learn' is not installed. Run: pip install imbalanced-learn")

# Brain emoji favicon as base64 SVG
FAVICON = "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🧠</text></svg>"


def create_app():
    """Create and configure the Dash application."""

    # Initialize app with Bootstrap and Font Awesome
    app = dash.Dash(
        __name__,
        external_stylesheets=[
            dbc.themes.BOOTSTRAP,
            "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"
        ],
        suppress_callback_exceptions=True,
        title="NeuroPredict AI - Alzheimer's Risk Assessment",
        update_title=None  # Prevents "Updating..." text in tab
    )

    # Set custom favicon
    app._favicon = FAVICON

    # Build layout
    app.layout = html.Div([
        # URL component for theme initialization
        dcc.Location(id='url', refresh=False),

        # Animated Background
        html.Div(className="bg-animated"),

        # Theme Toggle Button (Fixed Position)
        create_theme_toggle(),

        # Main Container
        dbc.Container([
            # Header
            create_header(),

            # Info Banner
            create_info_banner(),

            # Feature Input Cards
            html.Div(get_all_feature_cards()),

            # Predict Button
            create_predict_button(),

            # Result Output
            dbc.Row([
                dbc.Col([
                    dbc.Spinner(
                        html.Div(id="prediction-output"),
                        color="primary",
                        spinner_style={"width": "3rem", "height": "3rem"}
                    )
                ], xs=12, md=10, lg=8, className="mx-auto")
            ]),

            # Footer
            create_footer()

        ], fluid=True, style={"maxWidth": "1200px"})
    ], id="main-container")

    # Register callbacks
    register_callbacks(app)

    return app


# Create app instance
app = create_app()
server = app.server  # For deployment (Gunicorn, etc.)

if __name__ == '__main__':
    app.run(debug=True)