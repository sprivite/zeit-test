from flask import Flask, Response
import folium

app = Flask(__name__)


m = folium.Map(location=[48.7, 13.8], zoom_start=5)
m.save('test.html')
t = open('test.html').read()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return t
