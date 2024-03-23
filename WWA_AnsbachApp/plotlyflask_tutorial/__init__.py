"""Initialize Flask app."""
from ddtrace import patch_all
from flask import Flask
from flask_assets import Environment

patch_all()



def init_app():
    """Construct core Flask application with embedded Dash app."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object("config.Config")
    assets = Environment()
    assets.init_app(app)
    
    # Initialize Plugins

    with app.app_context():
        # Import parts of our core Flask app
        from . import routes
        from .assets import compile_static_assets

        # Import Dash application
        from .plotlydash.Waterlevels import init_dashboard
        from .plotlydash.DepthProfiles import init_dashboard2
        from .plotlydash.MeanConcentrations import init_dashboard3
        from .plotlydash.SpecieRelationShips import init_dashboard4
        from .plotlydash.DepthProfileTrends import init_dashboard5
        app = init_dashboard(app)
        app2 = init_dashboard2(app)
        app3 = init_dashboard3(app)
        app4 = init_dashboard4(app)
        app5 = init_dashboard5(app)
        # Compile static assets
        compile_static_assets(assets)

        return app, app2,app3,app4,app5
