from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


@app.route('/')
def index():
    
    mars_data = mongo.db.mars_data.find_one()
    return render_template('index.html', mars_data=mars_data)


@app.route('/scrape')
def scrape():

    mars_data = mongo.db.mars_data
    data = scrape_mars.scrape()
    mars_data.update({}, data, upsert=True)

    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
 