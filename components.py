# components.py - UI component builders with Dark Mode support

from dash import html, dcc
import dash_bootstrap_components as dbc
from config import FEATURE_GROUPS


def create_input_field(feature):
    """Create an input field based on feature type."""
    id_name = {'type': 'input-field', 'index': feature['name']}
    unit = feature.get('unit', '')

    label = html.Div([
        html.Span(feature['label']),
        html.Span(f" ({unit})", className="input-unit") if unit else None
    ], className="input-label")

    if feature['type'] == 'number':
        input_comp = dbc.Input(
            id=id_name, type="number",
            value=feature.get('default', 0),
            min=feature.get('min'), max=feature.get('max'),
            step="any", className="form-control"
        )
    elif feature['type'] == 'dropdown':
        input_comp = dbc.Select(
            id=id_name, options=feature['options'],
            value=feature['options'][0]['value'],
            className="form-select"
        )
    elif feature['type'] == 'radio':
        input_comp = dbc.RadioItems(
            id=id_name, options=feature['options'],
            value=feature['options'][0]['value'],
            inline=True, className="mt-2"
        )
    else:
        input_comp = dbc.Input(id=id_name, className="form-control")

    return dbc.Col([
        html.Div([label, input_comp], className="input-group-custom")
    ], xs=12, sm=6, lg=4)


def create_feature_card(group_name, group_data, delay_index):
    """Create a feature card for a group of inputs."""
    features = group_data['features']
    icon = group_data['icon']
    color = group_data['color']

    inputs = [create_input_field(f) for f in features]

    return html.Div([
        html.Div([
            html.Div([
                html.I(className=f"fa-solid {icon}")
            ], className="card-icon", style={"background": color}),
            html.H3(group_name, className="card-title-custom")
        ], className="card-header-custom"),
        dbc.Row(inputs)
    ], className="feature-card", style={"animationDelay": f"{delay_index * 0.1}s"})


def create_theme_toggle():
    """Create the dark/light mode toggle button."""
    return html.Div([
        html.Button([
            html.I(className="fa-solid fa-moon moon-icon"),
            html.I(className="fa-solid fa-sun sun-icon")
        ], id="theme-toggle-btn", className="theme-toggle-btn", n_clicks=0)
    ], className="theme-toggle-wrapper")


def create_header():
    """Create the app header."""
    return html.Div([
        html.Div([
            html.Div([
                html.I(className="fa-solid fa-brain", style={"fontSize": "2rem"})
            ], className="brain-logo"),
            html.Div([
                html.H1("NeuroPredict AI", className="app-title"),
                html.P("Advanced Alzheimer's Disease Risk Assessment", className="app-subtitle")
            ])
        ], className="logo-container", style={"flexDirection": "column"})
    ], className="app-header mt-4")


def create_info_banner():
    """Create the info banner."""
    return dbc.Alert([
        html.I(className="fa-solid fa-circle-info me-2"),
        "Enter patient information below for AI-powered risk assessment. All fields use clinically validated ranges."
    ], className="info-banner mb-4")


def create_predict_button():
    """Create the predict button."""
    return dbc.Row([
        dbc.Col([
            html.Button([
                html.I(className="fa-solid fa-wand-magic-sparkles me-2"),
                "Analyze Risk Profile"
            ], id="predict-btn", className="predict-btn w-100")
        ], xs=12, md=6, lg=4, className="mx-auto")
    ], className="my-4")


def create_footer():
    """Create the app footer."""
    return html.Div([
        html.Div([
            html.I(className="fa-solid fa-triangle-exclamation me-2"),
            html.Strong("Medical Disclaimer: "),
            "This tool is for educational and screening purposes only. ",
            "It does not constitute medical advice. Always consult a qualified ",
            "healthcare professional for diagnosis and treatment."
        ], className="disclaimer"),
        html.P([
            "© 2024 NeuroPredict AI • Built with ",
            html.I(className="fa-solid fa-heart", style={"color": "#ef4444"}),
            " using Machine Learning"
        ], className="mt-3 mb-0")
    ], className="app-footer")


def create_result_card(result):
    """Create the result display card."""
    prob_percent = result['probability'] * 100

    if result['is_positive']:
        return html.Div([
            html.Div([
                html.I(className="fa-solid fa-triangle-exclamation")
            ], className="result-icon"),
            html.H2("Elevated Risk Detected", className="result-title"),
            html.P(
                "Based on the provided data, the model indicates an elevated "
                "risk profile for Alzheimer's Disease.",
                className="result-description"
            ),
            html.Div([
                html.Div(style={"width": f"{prob_percent}%"}, className="probability-fill")
            ], className="probability-bar"),
            html.Div([
                html.Span("Risk Probability: ", style={"fontSize": "0.9rem"}),
                html.Span(f"{prob_percent:.1f}%", className="probability-text")
            ]),
            html.Div([
                html.I(className="fa-solid fa-lightbulb me-2"),
                "Recommendation: Consult with a neurologist for comprehensive evaluation."
            ], style={
                "marginTop": "1.5rem", "padding": "1rem",
                "background": "rgba(239,68,68,0.1)", "borderRadius": "10px",
                "fontSize": "0.9rem"
            })
        ], className="result-card result-positive")
    else:
        return html.Div([
            html.Div([
                html.I(className="fa-solid fa-shield-check")
            ], className="result-icon"),
            html.H2("Low Risk Profile", className="result-title"),
            html.P(
                "Based on the provided data, the model indicates a lower "
                "risk profile for Alzheimer's Disease.",
                className="result-description"
            ),
            html.Div([
                html.Div(style={"width": f"{prob_percent}%"}, className="probability-fill")
            ], className="probability-bar"),
            html.Div([
                html.Span("Risk Probability: ", style={"fontSize": "0.9rem"}),
                html.Span(f"{prob_percent:.1f}%", className="probability-text")
            ]),
            html.Div([
                html.I(className="fa-solid fa-heart-pulse me-2"),
                "Continue maintaining a healthy lifestyle and regular check-ups."
            ], style={
                "marginTop": "1.5rem", "padding": "1rem",
                "background": "rgba(16,185,129,0.1)", "borderRadius": "10px",
                "fontSize": "0.9rem"
            })
        ], className="result-card result-negative")


def create_error_alert(message, color="danger"):
    """Create an error alert."""
    return dbc.Alert([
        html.I(className="fa-solid fa-circle-xmark me-2"),
        message
    ], color=color, style={"borderRadius": "12px"})


def get_all_feature_cards():
    """Generate all feature cards."""
    return [
        create_feature_card(name, data, i)
        for i, (name, data) in enumerate(FEATURE_GROUPS.items())
    ]