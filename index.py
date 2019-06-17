from flask import request, Flask, Response
from jinja2 import Template
import pandas as pd


app = Flask(__name__)


country_centroids = pd.read_csv('country_centroids.csv.gz', index_col='name')
countries = list(country_centroids.index)
map_template = Template(open('country.html').read())
home_template = Template(open('index.html').read())


@app.route('/', methods=['GET'])
def viewer():

    country = request.args.get('country')
    if not country:
        response = home_template.render(countries='<br>'.join(countries))
        return Response(response, status=200)
        

    if country not in countries:
        return Response('Invalid country: {}!'.format(country), status=400)
        
    center = country_centroids.loc[country]
    lat, lon = center.latitude, center.longitude
    response = map_template.render(country=country, longitude=lon, latitude=lat)

    return Response(response, status=200, mimetype='text/html')
