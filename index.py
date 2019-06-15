from flask import request, Flask, Response
from jinja2 import Template
import pandas as pd

app = Flask(__name__)


country_centroids = pd.read_csv('country_centroids.csv.gz', index_col='name')
countries = list(country_centroids.index)
template = Template(open('index.html').read())


@app.route('/')
def home():

    return Response('Please enter a country in URL!<br>' + '<br>'.join(countries), status=200)


@app.route('/<country>', methods=['GET'])
def viewer(country):

    if country not in countries:
        return Response('Invalid country: {}!'.format(country), status=400)
        
    center = country_centroids.loc[country]
    lat, lon = center.latitude, center.longitude
    response = template.render(longitude=lon, latitude=lat)

    return Response(response, status=200)

