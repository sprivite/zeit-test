from flask import request, Flask, Response
from jinja2 import Template
import pandas as pd
import urllib

app = Flask(__name__)

global_counter = 0
chosen_countries = set([])
country_centroids = pd.read_csv('country_centroids.csv.gz', index_col='name')
countries = list(country_centroids.index)
map_template = Template(open('country.html').read())


@app.route('/', methods=['GET'])
def viewer():

    global global_counter, chosen_countries
    global_counter += 1

    country = request.args.get('country')
    if not country:
        response = map_template.render(
            country='Enter a country!',
            zoom=3,
            n_found=len(chosen_countries),
            n_countries=len(countries),
            latitude=52,
            longitude=13,
            countries='<br>'.join(sorted(chosen_countries)))
        return Response(response, status=200)

    if country == 'Arnesa':
        message = '<img width=400 src=https://rscdsvancouver.org/cms/wp-content/uploads/Hearts-In-Heart.png>'
        return Response(message)

    if country not in countries:
        return Response('Invalid country: {}!'.format(country), status=400)
        
    chosen_countries |= set([country])

    center = country_centroids.loc[country]
    lat, lon = center.latitude, center.longitude
    response = map_template.render(
        country=country,
        zoom=5,
        n_found=len(chosen_countries),
        n_countries=len(countries),
        longitude=lon,
        latitude=lat,
        countries='<br>'.join(sorted(chosen_countries)))

    return Response(response, status=200, mimetype='text/html')


@app.route('/counter')
def counter():
    return Response(str(global_counter), status=200)
