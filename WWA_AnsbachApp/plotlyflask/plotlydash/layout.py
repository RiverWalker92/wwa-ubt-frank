"""Plotly Dash HTML layout override."""
import os
STATIC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, 'static')


with open(os.path.join(STATIC_PATH, 'layout.html')) as f:
    html_layout = f.read()
