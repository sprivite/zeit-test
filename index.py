from flask import request, Flask, Response
from jinja2 import Template
import pandas as pd

app = Flask(__name__)


country_centroids = pd.read_csv('country_centroids.csv.gz', index_col='name')
template = Template(open('index.html').read())


@app.route('/', methods=['GET'])
def home():

    country = request.args.get('country')
    if country:
        try:
            center = country_centroids.loc[country]
            lat, lon = center.latitude, center.longitude
        except KeyError:
            return Response('Country not found!', status=400)
    else:
        return Response('Please enter a country!', status=200)

    response = template.render(longitude=lon, latitude=lat)
    return Response(response, status=200)

