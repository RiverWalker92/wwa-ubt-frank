"""Application entry point."""
from plotlyflask_tutorial import init_app

app,app2,app3,app4,app5= init_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0")
    app2.run(host="0.0.0.0")
    app3.run(host="0.0.0.0")
    app4.run(host="0.0.0.0")
    app5.run(host="0.0.0.0")
