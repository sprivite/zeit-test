from flask import Flask, Response
app = Flask(__name__)

@app.route('/europe')
def europe():
    return Response("<h1>Flask on Now</h1>", mimetype="text/html")
