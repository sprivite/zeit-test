from flask import Flask, Response
from jinja2 import Template
import pandas as pd

app = Flask(__name__)


country_centroids = pd.read_csv('country_centroids.csv.gz', index_col='name')
template = Template(open('index.html').read())


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):

    try:
        center = country_centroids.loc[path]
        lat, lon = center.latitude, center.longitude
    except KeyError:
        return Response('Country not found!', status=404)

    return template.render(longitude=lon, latitude=lat)

