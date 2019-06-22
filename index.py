from flask import request, Flask, Response
from jinja2 import Template
import pandas as pd


app = Flask(__name__)

global_counter = 0
chosen_countries = []
country_centroids = pd.read_csv('country_centroids.csv.gz', index_col='name')
countries = list(country_centroids.index)
map_template = Template(open('country.html').read())


@app.route('/', methods=['GET'])
def viewer():

    global global_counter
    global_counter += 1

    country = request.args.get('country')
    if not country:
        response = map_template.render(
            country='Enter a country!',
            zoom=3,
            latitude=52,
            longitude=13,
            countries='<br>'.join(sorted(chosen_countries)))
        return Response(response, status=200)
        

    if country not in countries:
        return Response('Invalid country: {}!'.format(country), status=400)
        
    chosen_countries.append(country)

    center = country_centroids.loc[country]
    lat, lon = center.latitude, center.longitude
    response = map_template.render(
        country=country,
        zoom=5,
        longitude=lon,
        latitude=lat,
        countries='<br>'.join(sorted(chosen_countries)))

    return Response(response, status=200, mimetype='text/html')


@app.route('/counter')
def counter():
    return Response(str(global_counter), status=200)
