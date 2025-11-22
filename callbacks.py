# callbacks.py - Dash callbacks with theme toggle support

from dash import Input, Output, State, ALL, clientside_callback


def register_callbacks(app):
    """Register all callbacks for the app."""

    # Import here to avoid circular imports
    from model_handler import model_handler
    from components import create_result_card, create_error_alert

    # --- Prediction Callback ---
    @app.callback(
        Output("prediction-output", "children"),
        Input("predict-btn", "n_clicks"),
        State({'type': 'input-field', 'index': ALL}, 'value'),
        State({'type': 'input-field', 'index': ALL}, 'id'),
        prevent_initial_call=True
    )
    def predict_disease(n_clicks, values, ids):
        """Handle prediction when button is clicked."""

        if not model_handler.is_loaded():
            return create_error_alert(
                "Model file not found. Please ensure 'alzheimers_model_data.pkl' is in the directory."
            )

        try:
            input_data = model_handler.prepare_input(values, ids)
            result = model_handler.predict(input_data)
            return create_result_card(result)

        except ValueError as e:
            return create_error_alert(str(e))
        except Exception as e:
            return create_error_alert(f"Prediction Error: {str(e)}", color="warning")

    # --- Dark Mode Toggle (Clientside Callback for Performance) ---
    app.clientside_callback(
        """
        function(n_clicks) {
            // Get current theme
            const html = document.documentElement;
            const currentTheme = html.getAttribute('data-theme');

            // Toggle theme
            if (currentTheme === 'dark') {
                html.setAttribute('data-theme', 'light');
                localStorage.setItem('theme', 'light');
            } else {
                html.setAttribute('data-theme', 'dark');
                localStorage.setItem('theme', 'dark');
            }

            return window.dash_clientside.no_update;
        }
        """,
        Output("theme-toggle-btn", "data-theme-clicked"),
        Input("theme-toggle-btn", "n_clicks"),
        prevent_initial_call=True
    )

    # --- Initialize Theme on Page Load ---
    app.clientside_callback(
        """
        function(pathname) {
            // Check localStorage for saved theme preference
            const savedTheme = localStorage.getItem('theme');

            // Check system preference if no saved theme
            if (savedTheme) {
                document.documentElement.setAttribute('data-theme', savedTheme);
            } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
                document.documentElement.setAttribute('data-theme', 'dark');
            }

            return window.dash_clientside.no_update;
        }
        """,
        Output("theme-toggle-btn", "data-theme-init"),
        Input("url", "pathname"),
        prevent_initial_call=False
    )