"""Routes for parent Flask app."""
from flask import current_app as app
from flask import render_template
from flask import render_template, redirect


@app.route("/")
def home():
    """Landing page."""
    return render_template(
        "index.jinja2",
        title="Franconian Lake Country Monitoring Data",
        description="A Combined effort of University Bayreuth and Wasser Wirtschaftsamt Ansbach.",
        template="home-template",      
    )
@app.route('/Waterlevels')
def dash1(): 
    return render_template('/Waterlevels.html', app_data=app_data)

@app.route('/DepthProfiles')
def dash2(): 
    return render_template('/DepthProfiles.html', app_data=app_data)

@app.route('/MeanConcentrations')
def dash3(): 
    return render_template('/MeanConcentrations.html', app_data=app_data)

@app.route('/SpecieRelations')
def dash4(): 
    return render_template('/SpecieRelations.html', app_data=app_data)

@app.route('/DepthProfileTrends')
def dash5(): 
    return render_template('/DepthProfileTrends.html', app_data=app_data)
                
